import importlib
import os
import shutil
from types import SimpleNamespace
from typing import Optional

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import gui
import utils
from widget import Widget

class Server:
    def __init__(self):
        # Use a service account to authenticate
        firebase_admin.initialize_app(credentials.Certificate("service_account.json"))
        client = firestore.client()
        self.systems = client.collection("systems")

        self.widgets = []
        self.systems.on_snapshot(self.on_systems_change)
        self.server_doc = self.systems.document("server")
        self.state_doc = client.collection("state").document("state")
        self.deps_doc = client.collection("dependencies").document("dependencies")
        self.state = {}
        self.state_doc.on_snapshot(self.on_state_change)

        # Set up the listener for changes to the server document
        self.server_doc.on_snapshot(self.on_change)

        # Start the GUI
        gui.GUI(self)

    def on_systems_change(self, docs, _1, _2):
        def is_widget(doc) -> bool:
            try:
                return doc.get("type") != "server"
            except KeyError:
                return True

        self.widgets = [
            Widget(
                id = doc.id,
                name = doc.to_dict().get("name"),
                type = doc.to_dict().get("type"),
                photo_id = doc.to_dict().get("photo_id"),
                dependencies = doc.to_dict().get("dependencies"),
                events = doc.to_dict().get("events"),
                server = self
            )
            for doc in docs if is_widget(doc)
        ]
        print(self.widgets)

    def on_state_change(self, docs, _1, _2):
        self.state = docs[0].to_dict()

    def on_change(self, _0, _1, _2):
        # Load the events raised to the server, and handle them in order
        server_snap = self.server_doc.get()
        events = utils.get_events(server_snap)
        for event in events:
            self.handle_event(event)

        # After handling all events, clear the event queue
        doc_dict = server_snap.to_dict()
        doc_dict["events"] = []
        self.server_doc.set(doc_dict)

    def handle_event(self, event):
        # Wrap the entire handler in a try/catch, since the user's code could always crash
        try:
            print("Received: {}".format(event))

            # Load the module of the widget sending the event
            widget = self.get_widget(name = event["sender"])
            module = load_widget_module(widget.id)

            # Get the function that corresponds to the event's type
            fun = getattr(module, event["type"].lower())

            # Wrap the widgets and state in a SimpleNamespace, to allow dot notation access
            widgets_wrapper = SimpleNamespace(**{widget.name: widget for widget in self.widgets})
            state_wrapper = SimpleNamespace(**self.state)

            # Invoke the function with the event's message
            fun(widgets_wrapper, state_wrapper, event["message"])
            self.state_doc.set(vars(state_wrapper))
        except Exception as e:
            print("Error handling event: {} - {}".format(type(e), e))

    def handle_code_updated(self):
        widgets = [widget for widget in [self.get_widget(widget_id = filename.replace(".py", "")) for filename in utils.get_filenames("widgets")] if widget is not None]
        for widget in widgets:
            with open(f"widgets/{widget.id}.py") as f:
                code = f.read()
                deps = [tmp.id for tmp in widgets if f"widgets.{tmp.name}" in code]
                widget.update(dependencies = deps)

    def add_widget(self, widget_name: str, widget_type: str, photo_id: int):
        # Add widget to firebase
        widget = Widget(id = None, name = widget_name, type = widget_type, photo_id = photo_id, dependencies = [], events = [], server = self).create()

        # Copy the template into the widgets with the new filename
        shutil.copy2("templates/{}.py".format(widget_type), "widgets/{}.py".format(widget.id))

        # Update dependencies
        self.handle_code_updated()

    def delete_widget(self, widget_id):
        # Delete widget from firebase
        self.systems.document(widget_id).delete()

        os.remove(f"widgets/{widget_id}.py")

        # Update dependencies
        self.handle_code_updated()

    def get_widget(self, widget_id: Optional[str] = None, name: Optional[str] = None) -> Optional[Widget]:
        if widget_id is not None:
            matching = [widget for widget in self.widgets if widget.id == widget_id]
        elif name is not None:
            matching = [widget for widget in self.widgets if widget.name == name]
        else:
            print("Must pass in an ID or name")
            raise LookupError()

        return next(iter(matching), None)

def load_widget_module(widget_id):
    # Load the module, then reload it (in case there were code changes since the last event)
    module = importlib.import_module("widgets.{}".format(widget_id))
    importlib.reload(module)
    return module


if __name__ == "__main__":
    Server()

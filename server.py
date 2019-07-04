import importlib

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
        self.systems = firestore.client().collection("systems")
        self.server_doc = self.systems.document("server")
        self.state_doc = self.systems.document("state")
        self.state = self.state_doc.get().to_dict()

        # Set up the listener for changes to the server document
        self.server_doc.on_snapshot(self.on_change)

        # Start the GUI
        gui.GUI()

    def on_change(self, _0, _1, _2):
        # Load the events raised to the server, and handle them in order
        events = utils.get_events(self.server_doc)
        for event in events:
            self.handle_event(event)

        # After handling all events, clear the event queue
        self.server_doc.set({"events": []})

    def handle_event(self, event):
        # Wrap the entire handler in a try/catch, since the user's code could always crash
        try:
            print("Received: {}".format(event))

            # Load the module of the widget sending the event
            module = load_widget_module(event["sender"])

            # Get the function that corresponds to the event's type
            fun = getattr(module, event["type"].lower())

            # Invoke the function with the event's message
            fun(self.load_widgets(), self.state, event["message"])
            self.state_doc.set(self.state)
        except Exception as e:
            print("Error handling event: {} - {}".format(type(e), e))

    def load_widgets(self):
        # Create a dictionary from all of the widget files where the key is the widget's name, and the value is the Widget object (which can raise events, etc)
        return {widget_name: Widget(widget_name, self) for widget_name in [filename.replace(".py", "") for filename in utils.get_filenames("widgets")]}

def load_widget_module(filename):
    # Load the module, then reload it (in case there were code changes since the last event)
    module = importlib.import_module("widgets.{}".format(filename.replace(".py", "")))
    importlib.reload(module)
    return module


if __name__ == "__main__":
    Server()

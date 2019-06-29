import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import importlib
import gui

class Server:
    def __init__(self):
        # Use a service account
        firebase_admin.initialize_app(credentials.Certificate('service_account.json'))
        self.systems = firestore.client().collection('systems')
        self.server_doc = self.systems.document('server')
        self.server_doc.on_snapshot(self.on_change)

        gui.GUI()

    def on_change(self, _0, _1, _2):
        events = get_events(self.server_doc)
        for event in events:
            self.handle_event(event)
        self.server_doc.set({"events": []})

    def handle_event(self, event):
        try:
            print("Received: {}".format(event))
            module = load_widget_module(event["sender"])
            fun = getattr(module, event["type"].lower())
            fun(self.raise_event, event["message"])
        except Exception as e:
            print("Error handling event: {}".format(e))

    def raise_event(self, widget_name, event):
        event["sender"] = "server"
        print("Sending to {}: {}".format(widget_name, event))
        widget = self.systems.document(widget_name)
        events = get_events(widget)

        events.append(event)

        widget.set({
            "events": events
        })

def get_events(doc):
    try:
        return doc.get().to_dict()["events"]
    except (KeyError, TypeError) as e:
        print(e)
        return []

def load_widget_module(filename):
    module = importlib.import_module("widgets.{}".format(filename.replace(".py", "")))
    importlib.reload(module)
    return module


if __name__ == '__main__':
    Server()

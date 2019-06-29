import importlib

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import gui
import utils
from widget import Widget

class Server:
    def __init__(self):
        # Use a service account
        firebase_admin.initialize_app(credentials.Certificate('service_account.json'))
        self.systems = firestore.client().collection('systems')
        self.server_doc = self.systems.document('server')
        self.server_doc.on_snapshot(self.on_change)

        gui.GUI()

    def on_change(self, _0, _1, _2):
        events = utils.get_events(self.server_doc)
        for event in events:
            self.handle_event(event)
        self.server_doc.set({"events": []})

    def handle_event(self, event):
        try:
            print("Received: {}".format(event))
            module = load_widget_module(event["sender"])
            fun = getattr(module, event["type"].lower())
            fun(self.load_widgets(), event["message"])
        except Exception as e:
            print("Error handling event: {}".format(e))

    def load_widgets(self):
        widgets = {}
        for widget_name in [filename.replace(".py", "") for filename in utils.get_filenames("widgets")]:
            widgets[widget_name] = Widget(widget_name, self)
        return widgets

def load_widget_module(filename):
    module = importlib.import_module("widgets.{}".format(filename.replace(".py", "")))
    importlib.reload(module)
    return module


if __name__ == '__main__':
    Server()

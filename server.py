import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import importlib
import gui

# Use a service account
firebase_admin.initialize_app(credentials.Certificate('service_account.json'))
db = firestore.client()
systems = db.collection('systems')
server = systems.document('server')

def start():
    server.on_snapshot(on_change)

    gui.GUI(reload_widget)

def on_change(_0, _1, _2):
    events = get_events(server)
    for event in events:
        handle_event(event)
    server.set({"events": []})

def get_events(doc):
    try:
        return doc.get().to_dict()["events"]
    except (KeyError, TypeError) as e:
        print(e)
        return []

def handle_event(event):
    try:
        print("Received: {}".format(event))
        module = import_widget(event["sender"])
        fun = getattr(module, event["type"].lower())
        fun(raise_event, event["message"])
    except Exception as e:
        print("Error handling event: {}".format(e))

def raise_event(widget_id, event):
    event["sender"] = "server"
    print("Sending to {}: {}".format(widget_id, event))
    widget = systems.document(widget_id)
    events = get_events(widget)

    events.append(event)

    widget.set({
        "events": events
    })

def reload_widget(filename):
    module = import_widget(filename.replace(".py", ""))
    importlib.reload(module)

def import_widget(widget_name):
    return importlib.import_module("widgets.{}".format(widget_name))


if __name__ == '__main__':
    start()

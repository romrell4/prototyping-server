from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time

# Use a service account
firebase_admin.initialize_app(credentials.Certificate('service_account.json'))
db = firestore.client()
systems = db.collection('systems')
server = systems.document('server')

def start():
    while True:
        widget = input("Enter your target widget: ")
        if widget == "quit": break

        while True:
            event_type = input("Enter an event type: ")
            if event_type == "back": break

            while True:
                message = input("Enter a message you'd like to fire: ")
                if message == "back": break

                raise_event(widget, {"type": event_type, "message": message, "sender": "server"})
    # server.on_snapshot(on_change)

def on_change(docs, _1, _2):
    for doc in docs:
        events = get_events(doc)
        for event in events:
            handle_event(event)

def get_events(doc):
    try:
        return doc.get().to_dict()["events"]
    except (KeyError, TypeError):
        return []

def handle_event(event):
    print(event)
    # if
    # raise_event('widget1', {
    #     ""
    # })

def raise_event(widget_id, value):
    widget = systems.document(widget_id)
    events = get_events(widget)

    events.append(value)

    widget.set({
        "events": events
    })


if __name__ == '__main__':
    start()


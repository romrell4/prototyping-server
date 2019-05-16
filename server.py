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
    server.on_snapshot(on_change)

def on_change(docs, _1, _2):
    for doc in docs:
        events = get_events(doc)
        for event in events:
            handle_event(event)

def get_events(doc):
    try: return doc.get('events')
    except KeyError: return []

def handle_event(event):
    print(event)
    # if
    # raise_event('widget1', {
    #     ""
    # })

def raise_event(widget_id, value):
    events = get_events(systems.document(widget_id))

    events.append(value)

    server.set({
        "events": events
    })


if __name__ == '__main__':
    start()

    while True:
        time.sleep(100)


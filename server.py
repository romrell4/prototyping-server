import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
firebase_admin.initialize_app(credentials.Certificate('service_account.json'))
db = firestore.client()
systems = db.collection('systems')
server = systems.document('server')

def start():
    # while True:
    #     widget = input("Enter your target widget: ")
    #     if widget == "quit": break
    #
    #     while True:
    #         event_type = input("Enter an event type: ")
    #         if event_type == "back": break
    #
    #         while True:
    #             message = input("Enter a message you'd like to fire: ")
    #             if message == "back": break
    #
    #             raise_event(widget, {"type": event_type, "message": message, "sender": "server"})
    server.on_snapshot(on_change)
    input("Press any button to exit\n")

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
    print("Received: {}".format(event))
    if event["sender"] == "widget1":
        if event["type"] == "BUTTON_TAPPED":
            raise_event("widget2", {"type": "UPDATE_BUTTON_TEXT", "message": event["message"], "sender": "server"})

def raise_event(widget_id, value):
    print("Sending: {}".format(value))
    widget = systems.document(widget_id)
    events = get_events(widget)

    events.append(value)

    widget.set({
        "events": events
    })

if __name__ == '__main__':
    start()

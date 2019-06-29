import utils

class Widget:
    def __init__(self, name, server):
        self.name = name
        self.server = server

    def update_text(self, text):
        self.raise_event("UPDATE_TEXT", text)

    def speak(self, text):
        self.raise_event("SPEAK", text)

    def raise_event(self, event_type, message):
        event = {
            "sender": "server",
            "type": event_type,
            "message": message
        }
        print("Sending to {}: {}".format(self.name, event))
        widget = self.server.systems.document(self.name)
        events = utils.get_events(widget)

        events.append(event)

        widget.set({
            "events": events
        })

import utils

class Widget:
    def __init__(self, id: str, name: str, type: str, server):
        self.id = id
        self.filename = f"{id}.py"
        self.name = name
        self.type = type
        self.server = server

    def __str__(self) -> str:
        return f"{{id: {self.id}, name: {self.name}, type: {self.type}}}"

    def __repr__(self) -> str:
        return self.__str__()

    ### DISPLAY WIDGET

    def update_text(self, text):
        self.raise_event("UPDATE_TEXT", text)

    ### BUTTON WIDGET

    def update_button_text(self, text):
        self.raise_event("UPDATE_BUTTON_TEXT", text)

    ### AUDIO WIDGET

    def speak(self, text):
        self.raise_event("SPEAK", text)

    ### KNOB WIDGET

    def update_knob(self, progress):
        self.raise_event("UPDATE_KNOB_PROGRESS", progress)

    ### PRIVATE FUNCTIONS

    def raise_event(self, event_type, message):
        event = {
            "sender": "server",
            "type": event_type,
            "message": message
        }
        print("Sending to {}: {}".format(self.name, event))
        widget_doc = self.server.systems.document(self.id)
        widget = widget_doc.get()

        widget_dict = widget.to_dict()
        widget_dict["events"] = utils.get_events(widget) + [event]
        widget_doc.set(widget_dict)

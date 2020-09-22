from typing import List, Dict, Optional

class Widget:
    def __init__(self, id: Optional[str], name: str, type: str, dependencies: List[str], events: List[str], server):
        self.id = id
        self.filename = f"{id}.py"
        self.name = name
        self.type = type
        self.dependencies = dependencies
        self.events = events
        self.server = server

    def __str__(self) -> str:
        return f"{{id: {self.id}, name: {self.name}, type: {self.type}}}"

    def __repr__(self) -> str:
        return self.__str__()

    def create(self):
        _, new_doc = self.server.systems.add(document_data = {
            "name": self.name,
            "type": self.type,
            "dependencies": self.dependencies,
            "events": self.events
        })
        self.id = new_doc.id
        return self

    def update(self, name: Optional[str] = None, type: Optional[str] = None, dependencies: Optional[List[str]] = None, events: Optional[List[Dict]] = None, add_event: Optional[Dict] = None):
        current_doc = self.server.systems.document(self.id)
        widget_dict = current_doc.get().to_dict()
        if name is not None:
            widget_dict["name"] = name
        if type is not None:
            widget_dict["type"] = type
        if dependencies is not None:
            widget_dict["dependencies"] = dependencies
        if events is not None:
            widget_dict["events"] = events
        if add_event is not None:
            widget_dict["events"].append(add_event)
        current_doc.set(widget_dict)

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
        self.update(add_event = event)

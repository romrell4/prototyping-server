class Widget:
    def __init__(self, name, server):
        self.name = name
        self.server = server

    def update_text(self, text):
        self.server.raise_event(self.name, {"type": "UPDATE_TEXT", "message": text})

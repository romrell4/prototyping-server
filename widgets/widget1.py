def button_tapped(raise_event, message):
    raise_event("widget3", {"type": "SPEAK", "message": message})


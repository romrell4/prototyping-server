def button_tapped(raise_event, message):
    raise_event("jessica", {"type": "SPEAK", "message": "I'm annoying, so I say " + message})


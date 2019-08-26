def button_tapped(widgets, state, _):
    widgets["widget3"].speak("I would like to say " + state["text"])
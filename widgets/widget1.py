def button_tapped(widgets, state, message):
    widgets["widget3"].speak(state["prefix"] + " " + message)
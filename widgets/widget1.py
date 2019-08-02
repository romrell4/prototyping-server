def button_tapped(widgets, state, _):
    widgets["widget3"].speak(state.get("widget4_text", "This is a test"))
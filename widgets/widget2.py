def progress_updated(widgets, state, new_progress):
    state["prefix"] = "Knob was updated first"
    widgets["widget3"].speak("Widget 2 is now at {} percent!".format(new_progress))
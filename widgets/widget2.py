def knob_progress_updated(widgets, state, new_progress):
    widgets["widget3"].speak("Widget 2 is now at {} percent!".format(new_progress))
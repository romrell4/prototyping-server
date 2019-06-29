def knob_progress_updated(raise_event, new_progress):
    raise_event("widget3", {"type": "SPEAK", "message": "Widget 2 is now at {} percent!".format(new_progress)})



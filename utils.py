import os

def get_filenames(dir_name):
    return sorted([file for file in os.listdir(dir_name) if not file.startswith("__")])

def get_events(doc):
    try:
        return doc.get().to_dict()["events"]
    except (KeyError, TypeError) as e:
        print(e)
        return []
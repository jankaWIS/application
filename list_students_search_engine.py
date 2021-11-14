import json
import os, sys

if len(sys.argv) == 3:
    path = sys.argv[1]
    phrase = sys.argv[2]
elif len(sys.argv) == 2:
    path = '../wis-advanced-python-2021-2022/students'
    phrase = sys.argv[1]
else:
    print("Please run as: python list_students_search_engine.py path phrase")
    exit(0)

# phrase = "na"
# path = '../wis-advanced-python-2021-2022/students'

def find_phrase_students(path, phrase):
    findings = {}
    for filename in os.listdir(path):
        # print(filename)
        with open(os.path.join(path, filename)) as fh:
            data = json.load(fh)
        # check name only
        # if "name" in data.keys() and phrase in data["name"]:
        #     print(data["name"])
        # else:
        #     print(f"This filename ({filename}) does not have name or {phrase} is not in name.")
        # print(data)
        print("")
        # # both fail on None as an item
        # print([(key, val) for key, val in data.items() if (phrase in val) or (phrase in key)])
        # print({key:val for key, val in data.items() if (phrase in val) or (phrase in key)})

        used_keys = []
        for key in data.keys():
            # check keys
            if phrase in key:
                used_keys.append(key)
                print("Found in key: ", key, data[key])
            # check values, avoid the None
            if data[key]:
                if phrase in data[key]:
                    used_keys.append(key)
                    findings[filename] = {"values": data[key]}
                    print("Found in value: ", key, data[key])
        if used_keys:
            findings[filename] = {"keys": set(used_keys)}
        # print(findings)

    return findings



find_phrase_students(path, phrase)

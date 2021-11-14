import json
import os, sys

if len(sys.argv) == 2:
    path = sys.argv[1]
else:
    path = '../wis-advanced-python-2021-2022/students'

def test_students():
    for filename in os.listdir(path):
        # print(filename)
        with open(os.path.join(path, filename)) as fh:
            data = json.load(fh)
        if "name" in data.keys():
            print(data["name"])
        else:
            print("This filename does not have name", filename)
        print("")

test_students()

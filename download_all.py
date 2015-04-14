import json
import os
import requests

OUTPUT = "./quakeml/"

files = ["2002.json", "2003.json", "2004.json", "2005.json", "2006.json", "2007.json", "2008.json", "2009.json", "2010.json", "2011.json"]

contents = []

for filename in files:
    with open(filename, "rt") as fh:
        contents.extend(json.loads(fh.read())["ResultSet"]["Result"])

resource_names = [_i["resource_name"] for _i in contents]

for _i, resource_name in enumerate(resource_names):
    filename = os.path.join(OUTPUT, resource_name)
    if not filename.endswith(".xml"):
        filename += ".xml"
    if os.path.exists(filename):
        continue

    print("Downloading %i of %i..." % (_i, len(resource_names)))
    r = requests.get("http://teide:8080/xml/seismology/event/" + resource_name)
    if (r.status_code != 200):
        print("Failed....")
        continue

    with open(filename, "wt") as fh:
        fh.write(r.text)

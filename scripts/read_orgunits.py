import json

with open('./districts.json', 'r') as f:
    poes = json.loads(f.read())
    for orgunit in poes["organisationUnits"]:
        # print(orgunit["displayName"], ",", orgunit["id"], ",", orgunit["path"], ",", orgunit["parent"]["id"])
        print(orgunit["displayName"], "#", orgunit["id"], "#", orgunit["path"], "#", orgunit["parent"]["id"])

import json
import requests

raw = open("majors.json", "r")
rawJson = json.load(raw)

apiURL = "https://mydegree.ucdavis.edu/responsiveDashboard/api/audit"
major = "major"
params = {"studentId":"696969","school":"UG","degree":"BS","catalogYear":"2021","goals":[{"code":"MAJOR","value":major}],"classes":[]}
with open('bearer.token', 'r') as f:
    auth_token = f.readlines()[0]
hed = {'Authorization': 'Bearer ' + auth_token}

major = "LCSI"
params["goals"][0]["value"] = major
response = requests.post(apiURL, json=params, headers=hed)
responseJson = response.json()

for i in responseJson["blockArray"]:
    if i["requirementType"] == "MAJOR":
        for j in i["ruleArray"]:
            if j["ruleType"] == "Subset":
                for k in j["ruleArray"]:
                    if k["ruleType"] == "Course":
                        for l in k["requirement"]["courseArray"]:
                            print(l["discipline"] + "-" + l["number"])
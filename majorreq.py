import json
import requests
import sys

raw = open("majors.json", "r")
rawJson = json.load(raw)

#for i in rawJson["_embedded"]["majors"]:
#    print(i["description"])

apiURL = "https://mydegree.ucdavis.edu/responsiveDashboard/api/audit"
major = "major"
params = {"studentId":"696969","school":"UG","degree":"BS","catalogYear":"2021","goals":[{"code":"MAJOR","value":major}],"classes":[]}
with open('bearer.token', 'r') as f:
    auth_token = f.readlines()[0]
hed = {'Authorization': 'Bearer ' + auth_token}

if(len(sys.argv) > 1): 
    major = sys.argv[1]
else:
    major = "LCSI"
params["goals"][0]["value"] = major
response = requests.post(apiURL, json=params, headers=hed)
responseJson = response.json()

outputDict = {major : []}
outputFile = open("output/" + major + ".json", "w")
"""
courseReqsRaw = requests.get("https://mydegree.ucdavis.edu/responsiveDashboard/api/course-link?discipline=ECS&number=036A&", headers=hed)
courseReqs = courseReqsRaw.json()["courseInformation"]["courses"]
print(courseReqs[0]["prerequisites"])
"""

for i in responseJson["blockArray"]:
    if i["requirementType"] == "MAJOR":
        for j in i["ruleArray"]:
            if j["ruleType"] == "Subset":
                for k in j["ruleArray"]:
                    if k["ruleType"] == "Course":
                        print(k["label"])
                        outputDict[major].append({k["label"] : []})
                        for l in k["requirement"]["courseArray"]:
                            courseString = ""
                            courseReqsString = ""
                            if("numberEnd" in l):
                                print("\t" + l["discipline"] + "-" + l["number"] + "-" + l["numberEnd"])
                                courseString = l["discipline"] + "-" + l["number"] + "-" + l["numberEnd"]
                            else:
                                courseReqsRaw = requests.get("https://mydegree.ucdavis.edu/responsiveDashboard/api/course-link?discipline=" + l["discipline"] + "&number=" + l["number"] + "&", headers=hed)
                                courseReqs = courseReqsRaw.json()["courseInformation"]["courses"]
                                if "prerequisites" in courseReqs[0]:
                                    for m in courseReqs[0]["prerequisites"]:
                                        courseReqsString += m["connector"] + " " + m["leftParenthesis"] + m["subjectCodePrerequisite"] + "-" + m["courseNumberPrerequisite"] + m["rightParenthesis"] + " "
                                print("\t" + l["discipline"] + "-" + l["number"] + courseReqsString)
                                courseString = l["discipline"] + "-" + l["number"]
                            outputDict[major][len(outputDict[major])-1][k["label"]].append({"course" : courseString, "prerequisites" : courseReqsString.strip()})

                        if("except" in k["requirement"]):
                            print("\tEXCEPT:")
                            outputDict[major][len(outputDict[major])-1][k["label"]].append({"EXCEPT":[]})
                            for m in k["requirement"]["except"]["courseArray"]:
                                courseString = ""
                                if("numberEnd" in m):
                                    courseString = m["discipline"] + "-" + m["number"] + "-" + m["numberEnd"]
                                    print("\t\t" + courseString)
                                else:
                                    courseString = m["discipline"] + "-" + m["number"]
                                    print("\t\t" + courseString)
                                outputDict[major][len(outputDict[major])-1][k["label"]][len(outputDict[major][len(outputDict[major])-1][k["label"]])-1]["EXCEPT"].append(m["discipline"] + "-" + m["number"])
json.dump(outputDict, outputFile, indent=4)
outputFile.close()
raw.close()
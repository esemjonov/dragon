##DRAGONS 

import requests
import json
import xml.etree.ElementTree as ET
from pprint import pprint


fighturl = "http://www.dragonsofmugloar.com/api/game"
weatherurl = "http://www.dragonsofmugloar.com/weather/api/report/"


##GET A FIGHT
r = requests.get(fighturl)

fight = r.json()
print(fight["gameId"])
print(fight["knight"])

##GET WEATHER FOR FIGHT
wreq = weatherurl + str(fight["gameId"])
w = requests.get(wreq)

##PARSED WEATHER XML
tree = ET.fromstring(w.content)
weather = tree.find("code")
print(weather.text)


solutionurl = "http://www.dragonsofmugloar.com/api/game/" + str(fight["gameId"]) + "/solution"
print ("\n" +solutionurl +"\n")

draakon = {"dragon": {"scaleThickness":3,"clawSharpness":6,"wingStrength":8,"fireBreath":3}}

pprint(draakon)
s = requests.put(solutionurl, json=draakon)

#NEW
#print (s.status_code)
print(s.content )

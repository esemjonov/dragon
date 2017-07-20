##DRAGONS 

import requests
import json
import xml.etree.ElementTree as ET
from pprint import pprint

#####################################################
#NMR draakoni treenimine
#####################################################

def NORMAL_WEATHER_ADVANCED(knight):
    knight_modded= str({'armor': knight["armor"], 'attack': knight["attack"],  'endurance': knight["endurance"], 'agility': knight["agility"]})    
    knight_modded= knight_modded.replace("'",'"')
    knight_modded = json.loads(knight_modded)

    index=0
    for key, value in sorted(knight_modded.items(), key=lambda item: (item[1], item[0]), reverse=True):
        if index==0:
            value=value+2
        elif index==1 or index==2:
            value=value-1
        elif index==3:
            value=value+0

        if key == "attack":
            scaleThickness=value
        elif key == "armor":
            clawSharpness=value
        elif key == "agility":
            wingStrength = value
        elif key == "endurance":
            fireBreath = value
        index+=1
    draakon = {"dragon": {"scaleThickness":scaleThickness,"clawSharpness":clawSharpness,"wingStrength":wingStrength,"fireBreath":fireBreath}}    
    return draakon

#####################################################
#Ilma põhjal draakoni valik
#####################################################

def WEATHER(fight):
    weather_id=weatherurl + str(fight["gameId"])
    wather_request =requests.get(weather_id)
    xml_tree = ET.fromstring(wather_request.content) 
    weather = xml_tree.find("code")
    
    
       
    if weather.text == "NMR":        
        draakon=NORMAL_WEATHER_ADVANCED(fight["knight"])        
        fight_index = 1
    elif weather.text == "SRO":
        draakon = {}
        fight_index = 2
    elif weather.text == "HVA":
        draakon = {"dragon": {"scaleThickness":5,"clawSharpness":10,"wingStrength":5,"fireBreath":0}}
        fight_index = 3
    elif weather.text == "T E":
        draakon = {"dragon": {"scaleThickness":5,"clawSharpness":5,"wingStrength":5,"fireBreath":5}}
        fight_index = 4
    elif weather.text == "FUNDEFINEDG":
        draakon = {"dragon": {"scaleThickness":5,"clawSharpness":5,"wingStrength":5,"fireBreath":5}}
        fight_index = 5


    solutionurl = "http://www.dragonsofmugloar.com/api/game/" + str(fight["gameId"]) + "/solution"
    tulemus=requests.put(solutionurl, json=draakon).json()
    
    logging= "Status: {0}\tDragon: {1}\tKnight: {2}\tWeather: {3}".format(str(tulemus["status"]).ljust(10, " "),str(draakon).ljust(95, " "),str(fight).ljust(150, " "),weather.text)
    result_array.append(logging)
    return result_array

#####################################################
#Logifaili loomine
#####################################################

def LOGGING(result_array):
    logfile= open ("logfile.txt","w")
    for item in result_array:
        logfile.write("%s\n" % item)        
    logfile.close()      
    
    
    
#####################################################
#Põhi loop, sisendinfo kontroll
#####################################################
    
def MAIN(result_array):
    while True:    
        try:
            number_of_battles = int(input("Sisesta soovitud lahingute arv, positiivne täisarv: "))
            if number_of_battles <0:
                print ("Tegu ei ole positiivse täisarvuga, proovi uuesti")
                continue
            break
        except ValueError:
            print("Tegu ei ole täisarvuga, proovi uuesti")
    i=0
    
    while i<number_of_battles:
        fight = requests.get(fighturl).json()        
        result_array=WEATHER(fight)
        i+=1
    LOGGING(result_array)   # logi faili loomine
   
#####################################################
#Globaal muutujad
#####################################################
    
fighturl = "http://www.dragonsofmugloar.com/api/game"
weatherurl = "http://www.dragonsofmugloar.com/weather/api/report/"
result_array=[]
MAIN(result_array)

    

   

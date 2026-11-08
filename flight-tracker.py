import os, requests, json, time, geopy.distance, sys, base64, datetime, re, configparser 
from collections import namedtuple

# notification sent
def notify(link,message):
    
    payload = ""

    print(message)
    
    if message.airline:
        payload += message.airline + " " 

    payload += message.flightNum + "\n"

    if message.aircraft:
        payload += message.aircraft + "\n"
    
    if message.origin:
        payload+= message.origin + "->" + message.destination + "\n" 

    payload += "Altitude: " + str(message.altitude) + " ft"  
    
    print(payload)
            
    requests.post(link,payload)

 
# read config file
config = configparser.ConfigParser()
config.read("config.ini")
s = config["settings"]


feederUrl = s["feederUrl"]
lat = float(s["lat"])
lon = float(s["lon"])
adsbUrl = s["adsbUrl"]
aeroUrl = s["aeroUrl"]
aeroKey = s["aeroKey"]
notifyUrl = s["notifyUrl"]
secretUrl = s["secretUrl"]

myCoords = (lat,lon)
Plane = namedtuple("Plane",["flightNum","distance","altitude","aircraft","airline"])
Message = namedtuple("Message",["flightNum","altitude","airline","aircraft","origin","destination"])

while(1):
   
    # Clear Screen and Data
    os.system('clear')
    flightData = []
    payload = []
    
    # Load data into the program
    data = requests.get(feederUrl).json()

    for x in range(len(data['aircraft'])):

        # only add if if a latitude and altitude are available to pull
        if 'lat' in data['aircraft'][x] and 'alt_baro' in data['aircraft'][x]:
 
            # create a list of flight numbers, distance from myself, and altitude
            flightNum = data['aircraft'][x].get('flight','').strip()

            dataCoords = (data['aircraft'][x]['lat'],data['aircraft'][x]['lon'])
            distance = round(geopy.distance.distance(myCoords,dataCoords).nm,1)

            altitude = data['aircraft'][x]['alt_baro']
            aircraft = data['aircraft'][x].get('desc')
            airline = data['aircraft'][x].get('ownOp')

            flightData.append(Plane(flightNum,distance,altitude,aircraft,airline))

    # sort the list by distance
    if len(flightData) >= 1:
        
        flightData.sort(key=lambda p: p.distance)
        
        # print a timestamp to see when it last ran
        print(datetime.datetime.fromtimestamp(data['now']).strftime('%Y-%m-%d %I:%M:%S %p\n'))
        print(flightData[0])

        # if a plane is within 1.5nm we can hear it
        if flightData[0].distance < 1.5:
           
            flightNum = flightData[0].flightNum
           
            print("\nGathering info on flight",flightNum)
            print()
           
            altitude = flightData[0].altitude
            aircraft = flightData[0].aircraft
            airline = flightData[0].airline

            # hit the API to gather some more info. Only do it if there's a flightnumber
            if flightNum:
            
                apiCall = {"planes": [{"callsign": flightNum}]}
                response = requests.post(secretUrl,json=apiCall)
                data = response.json()

                print(json.dumps(data, indent=4))

                if data[0].get('_airports'):
                    origin = data[0]['_airports'][0]['iata']
                    destination = data[0]['_airports'][1]['iata']
                else:
                    origin = ""
                    destination = ""

            #payload = {'max_pages': 1}
            #auth_header = {'x-apikey':aeroKey}
            #data = requests.get(url, params=payload, headers=auth_header)
            #response = json.loads(data.text)
    
            #for x in range(len(response['flights'])):

                # find planes that are en route
            #    if response['flights'][x]['progress_percent'] != 0 and response['flights'][x]['progress_percent'] != 100:
                        
            #        airline = response['flights'][x]['operator']
            #        origin = response['flights'][x]['origin']['code']    
            #        destination = response['flights'][x]['destination']['code']
            #        aircraft = response['flights'][x]['aircraft_type']
            #        break

            payload.append(Message(flightNum,altitude,airline,aircraft,origin,destination))
            notify(notifyUrl,payload[0])

            # mute notifications so we're not hammered with them
            time.sleep(105)
    
    time.sleep(15)


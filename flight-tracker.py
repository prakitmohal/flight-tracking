import os, requests, json, time, geopy.distance, sys, base64, datetime, re, configparser 
from collections import namedtuple

# notification sent
def notify(link,message):
    
    payload = []
    
    payload = message.airline + " " + message.flightNum + "\n"

    if messsage.aircraft:
        payload += message.aircraft + "\n"
    
    payload+= payload + message.origin + "->" + message.destination + "\n" + \
              "Altitude: " + str(message.altitude) + " ft"  
    
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

myCoords = (lat,lon)
Plane = namedtuple("Plane",["flightNum","distance","altitude","aircraft"])
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
            flightNum = data['aircraft'][x].get('flight','').strip() or None

            dataCoords = (data['aircraft'][x]['lat'],data['aircraft'][x]['lon'])
            distance = round(geopy.distance.distance(myCoords,dataCoords).nm,1)

            altitude = data['aircraft'][x]['alt_baro']
            aircraft = data['aircraft'][x].get('desc') or None

            flightData.append(Plane(flightNum,distance,altitude,aircraft))

    # sort the list by distance
    if len(flightData) >= 1:
        
        flightData.sort(key=lambda p: p.distance)
        print(datetime.datetime.fromtimestamp(data['now']).strftime('%Y-%m-%d %I:%M:%S %p'))

        for x in range(len(flightData)):
            print (x,flightData[x])
   
        # if a plane is within 1.5nm we can hear it
        if flightData[0].distance < 1.5:
           
            flightNum = flightData[0].flightNum
            
            print("gathering info on flight ",flightNum)
           
            altitude = flightData[0].altitude
            aircraft = flightData[0].aircraft
             
            # hit the API to gather some more info
            url = adsbUrl + flightNum
            data = requests.get(url).json()
            airline = data['response']['flightroute']['airline']['name']
            origin = data['response']['flightroute']['origin']['iata_code']
            destination = data['response']['flightroute']['destination']['iata_code']

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


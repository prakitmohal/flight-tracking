import os, requests, json, time, geopy.distance, sys, base64, datetime, re

# slack test
def slackTest(link,message):
    
    title = "PLANE DETECTED :airplane:"
    slackData = {
 
        "username": "Testing",
        "attachments": [
            {
                "color": "#FF0000",
                "fields": [
                    {
                        "title": title,
                        "value": message,
                        "short": "false",
 
                    }
                ]
            }
        ]
    }
     
    # Size of the slack data
    byte_length = str(sys.getsizeof(slackData))
    headers = {'Content-Type': "application/json",
               'Content-Length': byte_length}
     
    # Posting requests after dumping the slack data
    response = requests.post(link, data=json.dumps(slackData), headers=headers)

 
# read config file
config = open("config.txt","r")
link = config.readline().strip()
lat = config.readline()
lon = config.readline()
slackLink = config.readline().strip()
apiKey = config.readline().strip()
myCoords = (lat,lon)
config.close()


while(1):
   
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    
    # Load data into the program
    url = requests.get(link)
    data = json.loads(url.text)

    flightData = []
    for x in range(len(data['aircraft'])):

        # create a list of flight numbers, distance from myself, and altitude
        if 'lat' in data['aircraft'][x] and 'flight' in data['aircraft'][x] and 'alt_baro' in data['aircraft'][x]:
        
            flightNum = data['aircraft'][x]['flight']
            flightNum = flightNum.strip()

            dataCoords = (data['aircraft'][x]['lat'],data['aircraft'][x]['lon'])
            distance = round(geopy.distance.distance(myCoords,dataCoords).nm,1)

            altitude = data['aircraft'][x]['alt_baro']

            # only log if altitude < 15,000
            if altitude < 15000:
                flightData.append([flightNum,distance,altitude])

    # sort the list by distance
    entries = len(flightData)
    
    if entries >= 1:
        
        flightData.sort(key = lambda x: x[1])

        print (datetime.datetime.fromtimestamp(data['now']).strftime('%Y-%m-%d %H:%M:%S'))

        for x in range(entries):
            print (flightData[x])
   
        # if a plane is within 1.5nm we can hear it
        if flightData[0][1] < 1.5:
            
            flightNum = flightData[0][0]
            print ("Can you hear this plane: ",flightNum)

            # determine if the flight is a registration code or flight number to lookup
            # if it starts with N followed by a number assume it's a reg. Thanks Spirit Airlines 
            if re.match('^N[0-9]',flightNum):
                message = flightNum
            else:
                # This is a flight number lets look it up
                apiUrl = "https://aeroapi.flightaware.com/aeroapi/flights/" + flightNum
                payload = {'max_pages': 1}
                auth_header = {'x-apikey':apiKey}
                data = requests.get(apiUrl, params=payload, headers=auth_header)
                response = json.loads(data.text)

                for x in range(len(response['flights'])):

                    # find planes that are en route
                    if response['flights'][x]['progress_percent'] != 0 and response['flights'][x]['progress_percent'] != 100:
                        
                        origin = response['flights'][x]['origin']['code']    
                        destination = response['flights'][x]['destination']['code']
                        aircraft = response['flights'][x]['aircraft_type']
                        break

                message = flightNum + " " + origin + " " + destination + " " + aircraft 

            slackTest(slackLink,message)

            # mute notifications so we're not hammered with them
            time.sleep(105)
    
    time.sleep(15)


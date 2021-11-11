import os, requests, json, time, geopy.distance, sys, requests, base64, datetime

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
myCoords = (lat,lon)
config.close()


while(1):
   
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
            
            flightData.append([flightNum,distance,data['aircraft'][x]['alt_baro']])

    # sort the list by distance
    entries = len(flightData)
    
    if entries >= 1:
        
        flightData.sort(key = lambda x: x[1])

        print (datetime.datetime.fromtimestamp(data['now']).strftime('%Y-%m-%d %H:%M:%S'))

        for x in range(entries):
            print (flightData[x])
   
        # if a plane is within 1nm and under 10,000 feet we can hear it
        if flightData[0][1] < 1 and flightData[0][2] < 10000:
            print ("Can you hear this plane: ",flightData[0][0])
            slackTest(slackLink,flightData[0][0])

            # mute notifications so we're not hammered with them
            time.sleep(105)
    
    time.sleep(15)


# flight-tracking

What I'd eventually like to do is display the flight number, aircraft type
origin, and destination of any airplane I can hear onto one of those
scrolling text LED Display

I have created a slackbot in the meantime to test thsi proof of concept

You'll need python, geopy, and flightradar24
- pip3 install geopy
- pip3 install FlightRadarAPI

The config file currently has 4 lines

- The URL to retrieve the dump1090 JSON data
- The latitude of where you live
- The longitude of where you live
- The slack API url/key
- The flightaware API Key


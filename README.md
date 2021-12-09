# flight-tracking

What I'd eventually like to do is display the flight number, aircraft type,
origin, and destination of any airplane I can hear onto one of those
scrolling text LED Display

I have created a slackbot in the meantime to test this proof of concept

The assumption is that you already have piaware running on your raspberry pi

You'll need python, geopy, and requests
- pip3 install geopy
- pip3 install requests

You'll also need to register for a FlightAware API Key
https://flightaware.com/commercial/aeroapi

The config file currently has 5 lines

- The URL to retrieve the dump1090 JSON data
- The latitude of where you live
- The longitude of where you live
- The slack API url/key
- The flightaware API Key


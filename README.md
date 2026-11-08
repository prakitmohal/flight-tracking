# flight-tracking

What I'd eventually like to do is display the flight number, aircraft type,
origin, and destination of any airplane I can hear onto one of those
scrolling text LED Display

Right now this uses ntfy.sh to send me notifications, so I can test what will actually happen

The assumption is that you already have adsb.im running on your raspberry pi

You'll need python, geopy, and requests

You'll also need to register for a FlightAware API Key
https://flightaware.com/commercial/aeroapi

You can get by with the ADSB DB free API but the data isn't always correct, which I have temporarily

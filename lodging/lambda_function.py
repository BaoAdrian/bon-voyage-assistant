"""
Lodging API Lambda Function
"""

import json
import urllib.parse as urlparse
from urllib.parse import parse_qs
import base64

CLIENT_ID = ""
API_KEY = ""
API_ENDPOINT = ""

def lambda_handler(event, context):
    with open("lodging/hotels.json", "r") as f:
        json_data = json.load(f)

    # Extract city and state from event
    body = event["body"] # bG9jYXRpb25zPWNpdHkmbG9jYXRpb25zPXN0YXRlJmJ1ZGdldD05JnZhY2F0aW9uX3RpbWVzPXN0YXJ0X2RhdGUmdmFjYXRpb25fdGltZXM9ZW5kX2RhdGU=
    cities, states = extract_details(body)
    returned_body = {}

    # Loop through each provided city
    for i in range(len(cities)):
        city = cities[i].lower().replace(',', '')
        state = states[i].lower()

        city_hotels = json_data[city]
        hotel_dict = extract_hotels(city_hotels)
        avg_cost = find_average_cost(hotel_dict)
        cheapest = find_cheapest_lodging(hotel_dict)
        text = "Average cost for lodging in {}, {} is {} dollars, I recommend staying at {}, which costs {} dollars per night!".format(city, state, avg_cost, cheapest[0], cheapest[1])

        returned_body = {
            "hotels": city_hotels,
            "average_cost": avg_cost,
            "text": text
        }

    return {
        "statusCode": 200,
        "body": json.dumps(returned_body)
    }

def extract_details(body):
    """
    Takes body from JSON recieved from Alexa and parses attributes
    """
    # Decode event string
    base64_bytes = body.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')

    # NOTE: here, message = states=Arizona&cities=tucson%2C&budget=5&freetimes=5-June%3A9-June

    # Parse
    params = urlparse.urlparse("https://foo.com?" + message)

    # Extract city and state from params
    cities = parse_qs(params.query)['cities']
    states = parse_qs(params.query)['states']
    # free_times = parse_qs(params.query)['freetimes']
    return cities, states

# finds the average cost of all hotels within hotel_dict (which represents hotels in a given city)
def find_average_cost(hotel_dict):
    sum = 0
    count = 0
    for h in hotel_dict:
        sum += h["cost"]
        count += 1

    return sum/count

# returns the cheapest lodging; the name of the hotel first, followed by cost per night
def find_cheapest_lodging(hotel_dict):
    lowest = hotel_dict[0]["cost"]
    place = hotel_dict[0]["name"]
    for h in hotel_dict:
        if (h["cost"] < lowest):
            lowest = h["cost"]
            place = h["name"]

    return (place, lowest)

def extract_hotels(city):
    """
    Extracts all the returned places and formats a 
    list of dictionaries containing only the data the 
    is needed.

    @param response_json Full JSON object returned from GET Request
    @return formatted list of parsed JSON data
    """
    hotels = []
    for h in city:
        hotels.append(
            {
                "name": h["name"],
                "city": h["city"],
                "state": h["state"],
                "cost": h["cost"],
                "booked": h["booked"],
                "pets": h["pets"]
            }
        )
    return hotels
"""
Backend Lambda Function - Lodging Data

Lambda Function script to handle MOCK API Requests
to some Lodging API.

Currently uses a Data Store (hotels.json) to request 
accurate, researched, data on various hotels in sample
destinations.

@author Adrian Bao
@author Trey Bryant
"""
import json
import logging
import urllib.parse as urlparse
from urllib.parse import parse_qs
import base64

logger = logging.getLogger()

def lambda_handler(event, context):
    with open("hotels.json", "r") as f:
        json_data = json.load(f)

    # Extract city and state from event
    body = event["body"]
    cities, states = extract_details(body)
    logger.info("Body: {}".format(body))
    logger.info("Destination cities: {}".format(cities))
    logger.info("Destination states: {}".format(states))

    # Loop through each provided city
    returned_body = {}
    for i in range(len(cities)):
        city = cities[i].lower().replace(',', '')
        state = states[i].lower()

        city_hotels = json_data[city]
        hotel_dict = extract_hotels(city_hotels)
        avg_cost = find_average_cost(hotel_dict)
        cheapest = find_cheapest_lodging(hotel_dict)
        text = "Average cost for lodging in {}, {} is {} dollars, I recommend staying at {}, which costs {} dollars per night!".format(city, state, avg_cost, cheapest[0], cheapest[1])

        city_body = {
            "hotels": city_hotels,
            "average_cost": avg_cost,
            "text": text
        }

        if city not in returned_body:
            returned_body[city] = city_body

    return {
        "statusCode": 200,
        "body": json.dumps(returned_body)
    }

def extract_details(body):
    """
    Takes body from JSON recieved from Alexa and parses attributes

    @param body Body from Alexa-triggered Lambda
    @return parsed destination cities/states for Data Store Request
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

def find_average_cost(hotel_dict):
    """
    Finds the average cost of all hotels within the area of
    the requested destination city from the collected data set 

    @param hotel_dict Mock Hotel Data collected from Data Store
    """
    sum = 0
    count = 0
    for h in hotel_dict:
        sum += h["cost"]
        count += 1
    return sum/count

def find_cheapest_lodging(hotel_dict):
    """
    Returns tuple of data for the cheapest lodging option in
    the area.

    @param hotel_dict Modck Hotel Data collected from Data Store
    """
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
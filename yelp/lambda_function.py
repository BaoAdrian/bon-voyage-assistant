"""
Backend Lambda Function - Yelp API

Lambda Function script to handle API Requests
to Yelp API.

@author Adrian Bao
@author Trey Bryant
"""
import json
import urllib.parse as urlparse
from urllib.parse import parse_qs
import requests
import logging 
import base64

logger = logging.getLogger()

API_KEY = "XXXXXXXXXXX"
API_ENDPOINT = "https://api.yelp.com/v3/businesses/search"

cost_values = {
    "$": 7,
    "$$": 10,
    "$$$": 20,
    "$$$$": 25
}

def lambda_handler(event, context):
    """
    Handler function executed upon Lambda Function triggering.

    @param event Event data given from Lambda Event (JSON)
    @param context LambdaContext object
    @return HTTP Response after processing API Request
    """
    # Extract city and state from event
    body = event["body"]
    cities, states = extract_details(body)
    logger.info("Body: {}".format(body))
    logger.info("Destination Cities: {}".format(cities))
    logger.info("Destination States: {}".format(states))
    
    # Loop through each provided city
    returned_body = {}
    for i in range(len(cities)):
        city = cities[i].lower().replace(',', '')
        state = states[i].lower()

        # Sample Params
        params = {
            "location": city,
            "term": "restaurants",
            "limit": 5
        }

        requestHeaders = {
            "Content-type": "application/json",
            "Authorization": "Bearer " + API_KEY # Required for Auth
        }

        response = requests.get(API_ENDPOINT, 
            params=params, 
            headers=requestHeaders
        )

        # Extract data to return to Alexa
        response_json = json.loads(response.text)
        places = extract_places(response_json)
        average_cost = float(calculate_average_cost(places))

        # Alexa response
        text = "Average cost for food in {}, {} is ${}, I recommend checking out {} that has {} stars!".format(city, state, average_cost, places[0]["name"], places[0]["rating"])

        city_return_body = {
            "places": places,
            "average_cost": average_cost,
            "text": text
        }

        # Add new data
        if city not in returned_body:
            returned_body[city] = city_return_body

    logger.info("Response: {}".format(returned_body))

    return {
        "statusCode": 200,
        "body": json.dumps(returned_body)
    }

def extract_details(body):
    """
    Takes body from JSON recieved from Alexa and parses attributes

    @param body Body from Alexa-triggered Lambda
    @return parsed destination cities/states for Yelp API Request
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

def extract_places(response_json):
    """
    Extracts all the returned places and formats a 
    list of dictionaries containing only the data the 
    is needed.

    @param response_json Full JSON object returned from GET Request
    @return formatted list of parsed JSON data
    """
    places = []
    for place in response_json["businesses"]:
        places.append(
            {
                "name": place["name"],
                "cost": cost_values[place["price"]],
                "rating": place["rating"],
                "image_url": place["image_url"],
                "url": place["url"]
            }
        )
    return places

def calculate_average_cost(places):
    """
    Calculates the average cost across the places returned 
    from API GET Request. 

    @param places List of places returned from GET Request
    @return average cost across all returned places
    """
    cost = 0
    for place in places:
        cost += int(place["cost"])
    return cost/len(places)

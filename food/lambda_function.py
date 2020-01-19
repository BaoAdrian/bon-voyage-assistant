"""
Yelp API Lambda Function
"""
import json
import urllib.parse as urlparse
from urllib.parse import parse_qs
import requests
import logging 
import base64

logger = logging.getLogger()

CLIENT_ID = "zncWZ_dgf8To2adNhAF4nw"
API_KEY = "4B0KBKAjf7_iXHZOV4XToA4tRBH72q-IinOncFSvEEc0_phmYVssCUYodQPoJXwkCo6TwFx4G4z-o4oTDII3wgsYFU_aikS5BlTbqRHICn4pAG5JF0HSs8vVplwjXnYx"
API_ENDPOINT = "https://api.yelp.com/v3/businesses/search"

cost_values = {
    "$": 7,
    "$$": 10,
    "$$$": 20,
    "$$$$": 25
}

def lambda_handler(event, context):
    # print(event)
    logger.info("Event: {}".format(event))

    # Extract city and state from event
    city, state = extract_details(event)

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
    text = "Average cost for food in {}, {} is ${}, I recommend checking out {} that has {} stars!".format(city, state, average_cost, places[0]["name"], places[0]["rating"])

    returned_body = {
        "places": places,
        "average_cost": average_cost,
        "text": text
    }

    return {
        "statusCode": 200,
        "body": json.dumps(returned_body)
    }

def extract_details(event):
    """
    TODO: Implement
    """
    city, state = "Tucson", "Arizona"

    # Decode event string
    base64_bytes = event["body"].encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')

    logger.info("Body: {}".format(message))
    # print("Message: {}".format(message))

    # Parse
    t = urlparse.urlparse("https://foo.com?" + message)
    # print(t)
    # print(parse_qs(t.query)['city']) # Extract city


    return city, state

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

if __name__ == "__main__":
    with open("t.json", "r") as f:
        data = json.load(f)
        lambda_handler(data, None)
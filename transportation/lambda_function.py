"""
Transportation API Lambda Function
"""

import json
import urllib.parse as urlparse
from urllib.parse import parse_qs
import base64

def lambda_handler(event, context):
    with open("transport.json", "r") as f:
        json_data = json.load(f)

    # Extract city and state from event
    body = event["body"] # bG9jYXRpb25zPWNpdHkmbG9jYXRpb25zPXN0YXRlJmJ1ZGdldD05JnZhY2F0aW9uX3RpbWVzPXN0YXJ0X2RhdGUmdmFjYXRpb25fdGltZXM9ZW5kX2RhdGU=
    cities, states = extract_details(body)
    returned_body = {}

    # Loop through each provided city
    for i in range(len(cities)):
        city = cities[i].lower().replace(',', '')
        state = states[i].lower()

        city_trans = json_data[city]
        trans_dict = extract_options(city_trans)
        most_available = most_available_transport(trans_dict)
        text = "One of the most available modes of transport in {}, {} is by {}, with an average cost of {} dollars!".format(city, state, most_available[0], most_available[1])

        returned_body = {
            "transportation": city_trans,
            "most_available": most_available[1],
            "text": text
        }

    return {
        "statusCode": 200,
        "body": json.dumps(returned_body)
    }

# returns the most available transportation; the name of the method of transport, followed by average cost
def most_available_transport(trans_dict):
    most = trans_dict[0]["availability"]
    method = trans_dict[0]["name"]
    for t in trans_dict:
        if (t["availability"] > most):
            most = t["cost"]
            method = t["name"]

    return (method, most)

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

def extract_options(city):
    """
    Extracts all the returned places and formats a 
    list of dictionaries containing only the data the 
    is needed.

    @param response_json Full JSON object returned from GET Request
    @return formatted list of parsed JSON data
    """
    transportation = []
    for t in city:
        transportation.append(
            {
                "name": t["name"],
                "cost": t["cost"],
                "availability": t["availability"]
            }
        )
    return transportation
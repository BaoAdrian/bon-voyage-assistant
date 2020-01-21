"""
Backend Lambda Function - Transportation Data

Lambda Function script to handle MOCK API Requests
to some Transportation API.

Currently uses a Data Store (transport.json) to request 
accurate, researched, data on various public modes of 
transporation in sample destinations.

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
    """
    Handler function executed upon Lambda Function triggering.

    @param event Event data given from Lambda Event (JSON)
    @param context LambdaContext object
    @return HTTP Response after processing API Request
    """
    with open("transport.json", "r") as f:
        json_data = json.load(f)

    # Extract city and state from event
    body = event["body"] 
    cities, states = extract_details(body)
    logger.info("Body: {}".format(body))
    logger.info("Destination cities: {}".format(cities))
    logger.info("Destination states: {}".format(states))
    
    returned_body = {}

    # Loop through each provided city
    for i in range(len(cities)):
        city = cities[i].lower().replace(',', '')
        state = states[i].lower()

        city_trans = json_data[city]
        trans_dict = extract_options(city_trans)
        most_available = most_available_transport(trans_dict)
        text = "One of the most available modes of transport in {}, {} is by {}, with an average cost of {} dollars!".format(city, state, most_available[0], most_available[1])

        curr_body = {
            "transportation": city_trans,
            "most_available": most_available[1],
            "text": text
        }
        
        if city not in returned_body:
            returned_body[city] = curr_body

    logger.info("Response: {}".format(returned_body))

    return {
        "statusCode": 200,
        "body": json.dumps(returned_body)
    }

def most_available_transport(trans_dict):
    """
    Returns the most available transportation gathered
    from the transportation data provided.
    
    @param trans_dict Transportation Data provided 
    @return the most available mode of public transportation
    """
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
"""
Backend Lambda Function - Flight Engine

Lambda Function script to handle API Requests
to American Airlines Flight-Engine API.

@author Adrian Bao
@author Trey Bryant
"""
import json
import requests
import math
import urllib.parse as urlparse
from urllib.parse import parse_qs
import base64
from datetime import datetime
import logging

logger = logging.getLogger()

LIMIT = 10

def lambda_handler(event, context):
    """
    Handler function executed upon Lambda Function triggering.

    @param event Event data given from Lambda Event (JSON)
    @param context LambdaContext object
    @return HTTP Response after processing API Request
    """
    API_ENDPOINT = "https://flight-manager-api.herokuapp.com"
    PARAM = "/flights?date="

    # Extract body
    body = event["body"]
    logger.info("Body: {}".format(body))
    
    # Gather requested date from event body and update API Request URL
    date_str = extract_details(body)
    PARAM += date_str
    API_ENDPOINT += PARAM
    logger.info("API Endpoint: {}".format(API_ENDPOINT))

    # Perform GET request to Flight-Engine API
    flight_api_response = requests.get(API_ENDPOINT)
    api_json = json.loads(flight_api_response.text)
    
    # Extract requested destination (cities, states) from body
    origin_city, origin_state = "Los Angeles", "California" # Current origin
    dest_cities, dest_states = extract_destinations(body)

    # For each destination, extract API data to return
    returned_body = {}
    for i in range(len(dest_cities)):
        dest_city = dest_cities[i]
        dest_state = dest_states[i]

        filtered_res = filter_by_destination(api_json, dest_city, dest_state)
        average_cost = math.floor(calculate_average_cost(filtered_res))

        flight_data = {
            "average_cost": average_cost,
            "origin": {
                "city": origin_city,
                "state": origin_state
            },
            "destination": {
                "city": dest_city,
                "state": dest_state
            },
            "text": "some response for Alexa"
        }
        returned_body[dest_city] = flight_data

    return {
        "statusCode": 200,
        "body": json.dumps(returned_body)
    }

def extract_destinations(body):
    """
    Takes body from JSON recieved from Alexa and parses destination
    details from the Flight-Engine GET request.

    @param body Response body from the Flight-Engine GET request
    @return Lists of destination cities/states
    """
    # Decode event string
    base64_bytes = body.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')

    # NOTE: here, message = states=Arizona&cities=tucson%2C&budget=5&freetimes=5-June%3A9-June

    params = urlparse.urlparse("https://foo.com?" + message)

    # Extract city and state from params
    cities = parse_qs(params.query)['cities']
    states = parse_qs(params.query)['states']
    # free_times = parse_qs(params.query)['freetimes']
    return cities, states

def extract_details(body):
    """
    Takes body from JSON recieved from Alexa and parses date
    needed for the Flight-Engine GET request.
    """
    # Decode event string
    base64_bytes = body.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')

    # NOTE: here, message = states=Arizona&cities=tucson%2C&budget=5&freetimes=5-June%3A9-June

    # Parse
    params = urlparse.urlparse("https://foo.com?" + message)

    # Extract city and state from params
    freetimes = parse_qs(params.query)['freetimes']
    split_times = freetimes[0].split(':')

    start_date = split_times[0]
    date_params = start_date.split('-')
    year = "2020"
    day = int(date_params[0])
    
    if day < 10:
        day_string = "0"+str(day)
    else:
        day_string = str(day)

    month = extract_month(date_params[1])

    date_str = "{}-{}-{}".format(year, month, day_string)
    return date_str

def extract_month(string_month):
    """
    Converts the month give from Alexa Lambda Function
    from the string format ("May") to integer format ("5")

    @param string_month String formatted month (e.g: "May")
    @return integer formatted month (e.g: "5")
    """
    month = string_month.lower()
    if month == "january":
        return "01"
    elif month == "febraury":
        return "02"
    elif month == "march":
        return "03"
    elif month == "april":
        return "04"
    elif month == "may":
        return "05"
    elif month == "june":
        return "06"
    elif month == "july":
        return "07"
    elif month == "august":
        return "08"
    elif month == "september":
        return "09"
    elif month == "october":
        return "10"
    elif month == "november":
        return "11"
    else:
        return "12"

def filter_by_destination(res_json, city, state):
    """
    Filters the returned data by the provided destination
    city
    
    @param res_json JSON data from Flight-Engine response
    @param city provided destination city
    @param state provided destination state
    @return filtered JSON data containing only destination data
    """
    # Save filtered results
    filter_res = []
    for res in res_json:
        if res["destination"]["city"].lower() == city.lower():
            filter_res.append(res)
    return filter_res

def calculate_average_cost(filtered_res):
    """
    Calculates the average cost of the supplied filtered
    results from the Flight-Engine response

    @param filtered_res JSON data filtered from API response
    @return average flight cost from the provided filtered data
    """
    cost = 0
    for flight in filtered_res:
        cost += int(flight["cost"])
    return cost/len(filtered_res)

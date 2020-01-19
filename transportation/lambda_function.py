"""
Transportation API Lambda Function
"""

import json

CLIENT_ID = ""
API_KEY = ""
API_ENDPOINT = ""

def lambda_handler(json_data, context):
    city, state = "Tucson", "Arizona"
    city_trans = json_data["Tucson"]
    trans_dict = extract_options(city_trans)
    most_available = most_available_transport(trans_dict)
    text = "One of the most available modes of transport in {}, {} is by {}, with an average cost of {} dollars!".format(city, state, most_available[0], most_available[1])

    print(text)

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

if __name__ == "__main__":
    with open("transportation/transport.json", "r") as f:
        data = json.load(f)
        lambda_handler(data, None)
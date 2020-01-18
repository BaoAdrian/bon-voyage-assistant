"""
Yelp API Lambda Function
"""

import json
import requests

CLIENT_ID = "zncWZ_dgf8To2adNhAF4nw"
API_KEY = "4B0KBKAjf7_iXHZOV4XToA4tRBH72q-IinOncFSvEEc0_phmYVssCUYodQPoJXwkCo6TwFx4G4z-o4oTDII3wgsYFU_aikS5BlTbqRHICn4pAG5JF0HSs8vVplwjXnYx"
API_ENDPOINT = "https://api.yelp.com/v3/businesses/search"

cost_values = {
    "$": 7,
    "$$": 10,
    "$$$": 20,
    "$$$$": 25,
    "$$$$$": 30 
}

def main():
    # Sample Params
    params = {
        "location": "Tucson"
    }

    requestHeaders = {
        "Content-type": "application/json",
        "Authorization": "Bearer " + API_KEY # Required for Auth
    }

    response = requests.get(API_ENDPOINT, 
        params=params, 
        headers=requestHeaders
        )

    # Example of data access
    response_json = json.loads(response.text)
    dollar_signs = response_json["businesses"][0]["price"]

    print("Dollar Signs: {}".format(dollar_signs))
    print("Average Cost: {}".format(cost_values[dollar_signs]))


if __name__ == "__main__":
    main()
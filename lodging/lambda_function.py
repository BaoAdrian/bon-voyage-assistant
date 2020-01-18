"""
XXXXX API Lambda Function
"""

import json
import requests

CLIENT_ID = ""
API_KEY = ""
API_ENDPOINT = ""

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


if __name__ == "__main__":
    main()
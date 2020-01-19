"""
Lodging API Lambda Function
"""

import json

CLIENT_ID = ""
API_KEY = ""
API_ENDPOINT = ""

def lambda_handler(json_data, context):
    city, state = "Tucson", "Arizona"
    city_hotels = json_data["Tucson"]
    hotel_dict = extract_hotels(city_hotels)
    avg_cost = find_average_cost(hotel_dict)
    cheapest = find_cheapest_lodging(hotel_dict)
    text = "Average cost for lodging in {}, {} is {} dollars, I recommend staying at {}, which costs {} dollars per night!".format(city, state, avg_cost, cheapest[0], cheapest[1])

    print(text)

    returned_body = {
        "hotels": city_hotels,
        "average_cost": avg_cost,
        "text": text
    }

    return {
        "statusCode": 200,
        "body": json.dumps(returned_body)
    }

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

if __name__ == "__main__":
    with open("lodging/hotels.json", "r") as f:
        data = json.load(f)
        lambda_handler(data, None)
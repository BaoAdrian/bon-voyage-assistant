# Lodging API Lambda Function
This Lambda Function extracts Mock data (researched for each city) to simulate the use of some Lodging API such as Expedia or Travelocity. Constructed a data store (`hotels.json`) used to retrieve data for each of the requested destination locations provided by Alexa.

Response data such as `cost` are be used to best determine recommendation to the user based on their requested destinations. Alexa will provide suggested lodging options around the area to visit that are cost-efficient in the area.

For the submission to HackArizona, `hotels.json` was used as the Data Store but some API options we investigated but were unable to utilize/setup in time were:
   - [Google Hotel API](https://developers.google.com/hotels/hotel-prices/api-reference/v20/hotels-api-v2)
   - [Trip Advisor](https://developer-tripadvisor.com/content-api/)


# Response
Sample response:
```
{
    "Chicago" : {
        "hotels": [
            {
                "name": "The River Hotel",
                "city": "Chicago",
                "state": "Illinois",
                "cost": 60, # per-night
                "booked": "False",
                "pets": "False",
            },
            ...
        ],
        "average_cost": 150, # of all local lodging
        "text": "Some response to Alexa"
    },
    ...
}
```

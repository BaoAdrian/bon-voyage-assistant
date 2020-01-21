# Transportation API Lambda Function
This Lambda Function extracts Mock data to simulate the use of some Transportation API such as Google Transit API. Constructed a data store (`transport.json`) used to retrieve data for each of the requested destination locations provided by Alexa.

Response data such as `cost` and `availability` are used to best determine recommendation to the user based on their requested destinations. Alexa will provide suggested transportation options around the area to visit that are cost-efficient and high in availability in the area.

For the submission to HackArizona, `transport.json` was used as the Data Store but some API options we investigated but were unable to utilize/setup in time were:
   - [Google Tranit API](https://developers.google.com/transit)
   - [Public Transit API](https://developer.here.com/documentation/transit/dev_guide/topics/what-is.html)


# Response
Sample response:
```
{
    "Chicago" : {
        "transportation": [
            {
                "name": "bus",
                "cost": 10,
                "availability": 5
            },
            ...
        ],
        "most_available": "bus", # of all public transit
        "text": "Some response to Alexa"
    },
    ...
}
```

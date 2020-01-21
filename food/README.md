# Yelp API Lambda Function
This Lambda Function performs a GET Request to the [`Yelp Fusion API`](https://www.yelp.com/fusion) to retrieve data for each of the requested destination locations provided by Alexa.

Response data such as `cost` and `rating` will be used to best determine recommendation to the user based on their requested destinations. Alexa will provide suggested restauraunts around the area to visit that are cost-efficient and highly rated in the area.

# Response
Sample response:
```
{
    "Chicago" : {
        "places": [
            {
                "name": "Olive Garden",
                "cost": 10, # per-person @ this place
                "rating": 4,
                "image_url": "some_image_to_display",
                "url": "some_url_to_visit"
            },
            ...
        ],
        "average_cost": 15, # of all local restaruants
        "text": "Some response to Alexa"
    },
    ...
}
```

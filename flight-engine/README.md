# Flight Engine Lambda Function
This Lambda Function performs a GET Request to the [Flight Engine](https://github.com/AmericanAirlines/Flight-Engine) API. This is an applicataion provided by American Airlines hosted on [`Heroku`](https://devcenter.heroku.com/) that provides flight data such as `origin`, `destination`, and `cost`. 

Lambda Function defined inside Alexa Skills Kit triggers this Lambda Function to retrieve flight data based on the User's interaction with Alexa.

# Response
Lambda Function response:
```
{
    "Chicago" : {
        "average_cost": 350,
        "origin": {
            "city": "Los Angeles",
            "state": "California"
        },
        "destination": {
            "city": "Chicago",
            "state": "Illinois"
        },
        "text": "Some response to Alexa"
    },
    ...
}
```

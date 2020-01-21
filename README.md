# Bon Voyage Assistant
This Alexa Skill-based application was developed as our **HackArizona 6.0 (2020)** submission and **achieved 2nd place** for the [`American Airlines Challenge`](https://github.com/AmericanAirlines/Flight-Engine/wiki/Hack-Arizona-2020) with the following details:
```
Thousands of people fly American each and every day. This awesome responsibility opens the door to incredible opportunities. Help us elevate the customer travel experience, boost operational efficiency and employee performance (baggage handling, gate agents, etc.), or enhance American's brand image with your innovative hacks!
```

And was judged using the following criteria:
```
- Likelihood of your app improving customer experience, boosting operational efficiency and employee performance, or enhancing brand image
- Look and Feel
- Functionality
- API Utilization (use our Flight Engine or some other source of data)
```

## Team Members
- Adrian Bao
   - [`Github`](https://github.com/BaoAdrian)
   - [`LinkedIn`](https://www.linkedin.com/in/baoadrian/)
- Trey Bryant
   - [`Github`](https://github.com/tr3ylbry)
   - LinkedIn
- Victora Metzler
   - Github
   - [`LinkedIn`](https://www.linkedin.com/in/victoria-metzler/)
- Jack Mittelmeir
   - [`Github`](https://github.com/jack-mitt)
   - [`LinkedIn`](https://www.linkedin.com/in/jack-mittelmeier-24068b178/)

# Summary
This application is an Alexa Skill-based app backed by AWS that provides a streamlined process for scheduling a vacation. It simplifies the planning process for a user looking to schedule a trip and wanting to quickly analyze their financial obligations for their destination. This includes the Flight, Lodging, Food, and Transportation for their destination(s). 

Upon interaction with the user, Alexa will provide them with a full cost-analysis of their prospective trip and even provide recommendations on lodging, places to eat, and even what modes of transportations to use based on their cost, availability, and rating!
 
With the use of several APIs, serverless computing and the power of Alexa, this application simplifies and streamlines the complexities of trip-planning, make traveling more accessible to everyone.

# Technology Stack
This project leverages the following tools and technologies to achieve its functionality:
- Serverless Computing
   - [`Alexa Skill Kit`](https://developer.amazon.com/en-US/alexa/alexa-skills-kit)
   - [`AWS Lambda`](https://aws.amazon.com/lambda/)
   - [`AWS S3`](https://aws.amazon.com/s3/) (Optional/Prospective)
   - [`DynamoDB`](https://aws.amazon.com/dynamodb/) (Optional/Prospective)
- APIs
   - American Airlines [`Flight-Engine`](https://github.com/AmericanAirlines/Flight-Engine/) (Deployed using Heroku)
   - [`Yelp Fusio API`](https://www.yelp.com/fusion)
   - Mock Data Stores for Lodging and Transportation
      - Prospective APIs such as Google Hotel API & Google Transit API will be incorporated in the future.

Note, mock data was utilized to represent the lodging and transportation data due to the limitation of free-access APIs for both sections and the time-limit for the submission of the HackArizona event. This was meant to simulate what data processing for those portions would appear like and how they would aid in processing with the Alexa commands.

# Backend Development
The backend for this project is supported using AWS Lambda Functions defined using Python that target multiple APIs to `GET` & `POST` data for various usages for our application. 

To incorporate interfacing with 4 seperate APIs and isolating those requests and processing, we decided to split each individual API interaction into its own Lambda Function that would accept incoming HTTP traffic through a configured API Gateway to parse parameters used to interface with the various APIs.

These Lambda Functions, in turn, would generate a customized response for the Alexa Skill Kit to handle and verbally relay the results to the user to assist them in their travel planning. An added benefit was the serverless aspect ensuring that no computing resources were wasted, instead, they were only triggered and activated when needed.

The main goal with this structure was to abstract the backend complexities with the various API calls being made and provide the user with a simple interaction with Alexa that would complete a powerful collection of data to financially plan an entire vacation stay based solely on a provided destination and budget.

# Future Enhancements
This project has tons of potential to expand and improve into a full-fledged travel assistant leveraging serverless compute with AWS, seamless architecture intergration with Alexa, & using various powerful APIs for helpful data requests being made to plan a trip!

Some ideas for future enhancements include:
- Find APIs for *Lodging* and *Transportation* to substitute the use of the Mock Data Store
- Enhance data collection and provide real-time analysis of ratings, proximites, filtering by expanding Alexa's capabilities to request for additional query parameters
- Introduce `DynamoDB` to persist Alexa Sessions across interactions
- Integrate [`Google Calender API`](https://developers.google.com/calendar) to allow detection of free-time, schedule notifications for automated searches, etc...
   - This could be an incredibly powerful integration as one could quickly analyze their viability of a trip in their current state and if it the result is not QUITE financially appropriate, the user can simply tell Alexa to "Check again in a week". Alexa could then setup a reminder in one week to trigger the backend processing once more and let the user know if anything has changed.
- Extend the query-functionality by allowing the user to have a *Purchase* or *Confirm Flight* option at the end if they are satisfied with the resulting data requests on all fronts.
- Expand to incorporate Amazon's Echo Show and its screen to present the user with real-time, visual, suggestions on flights, restaraunts, hotels, and public transportation resources.
- Much, much more!

# Content of this repo
Each directory within this repo corresponds to its associated component in the application. 
- `alexa-code` contains the code used to generate and execute the sessions processing for Alexa
- `flight-engine` contains the used to process API requests to American Airlines `Flight-Engine API`
- `lodging` contains the code used to process mock data store requests for Lodging information
- `transportation` contains the code used to process mock data store requests for Transportation information
- `yelp` contains the code used to process API requests to `Yelp Fusion API`
# -*- coding: utf-8 -*-

# Yo shouts out squad on this one
# Authors: Jack and Victoria
# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import requests
import ask_sdk_core.utils as ask_utils
import os
import json

from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_s3.adapter import S3Adapter
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
s3_adapter = S3Adapter(bucket_name=os.environ["S3_PERSISTENCE_BUCKET"])

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hi, I'm your hack arizona travel assistant. Would you like to add a city you would like to travel to, set your budget, add or remove vacation times, or check available trips?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class GetCityIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GetCityIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        attributes_manager = handler_input.attributes_manager
        city = slots["city"].value
        state = slots["state"].value
        speak_output = "Added {city} {state}. Do you have any more?".format(city=city, state=state)
        if "cities" in attributes_manager.session_attributes.keys():
            attributes_manager.session_attributes["cities"].append(city)
        else:
            attributes_manager.session_attributes["cities"] = []
            attributes_manager.session_attributes["cities"].append(city)
            
        if "states" in attributes_manager.session_attributes.keys():
            attributes_manager.session_attributes["states"].append(state)
        else:
            attributes_manager.session_attributes["states"] = []
            attributes_manager.session_attributes["states"].append(state)
        
        #store it 
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class GetMoreCitiesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("MoreCitiesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Ok what would you like to add?"
        
        #store it 
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                
                .response
        )

class NoMoreCitiesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("NoMoreCitiesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Ok, what is your budget?"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )  

class GetVacationDaysIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("GetVacationDaysIntent")(handler_input)
        
    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        attributes_manager = handler_input.attributes_manager
        
        startDay = slots["startDay"].value
        startMonth = slots["startMonth"].value
        endDay = slots["endDay"].value
        endMonth = slots["endMonth"].value

        
        speak_output = "Noted, you are free from {startMonth} {startDay} to {endMonth} {endDay}. Now say, check trips.".format(startMonth=startMonth, startDay=startDay, endMonth=endMonth, endDay=endDay)
        
        if "vacation_times" in attributes_manager.session_attributes.keys():
            attributes_manager.session_attributes["vacation_times"].append(startDay + "-" + startMonth + ":" + endDay + "-" + endMonth)
        else:
            attributes_manager.session_attributes["vacation_times"] = []
            attributes_manager.session_attributes["vacation_times"].append(startDay + "-" + startMonth + ":" + endDay + "-" + endMonth)
        
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class GetBudgetIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("GetBudgetIntent")(handler_input)
        
    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        attributes_manager = handler_input.attributes_manager
        
        budget = slots["budget"].value
        attributes_manager.session_attributes["budget"] = budget
        speak_output = "Got it, {budget} dollars. When are you free?".format(budget=budget)
        
        #store it
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class SetBudgetIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("SetBudgetIntent")(handler_input)
    
    def handle(self, handler_input):
        attributes_manager = handler_input.attributes_manager
        speak_output = "What would you like to set it to?"
        if "budget" in attributes_manager.session_attributes.keys():
            speak_output = "Your current budget is {budget}. What would you like to set it to?".format(attributes_manager.session_attributes["budget"])
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CheckTripsIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("CheckTripsIntent")(handler_input)
        
    def handle(self, handler_input):
        attributes_manager = handler_input.attributes_manager
        locations = []
        vacation_times = []
        
        json_new = {
            "states": attributes_manager.session_attributes["states"],
            "cities": attributes_manager.session_attributes["cities"],
            "budget": attributes_manager.session_attributes["budget"],
            "freetimes" : attributes_manager.session_attributes["vacation_times"]
        }
        r = requests.post("https://0zlru1ggpl.execute-api.us-east-2.amazonaws.com/default/flight-engine", json_new)
        r1 = requests.post("https://pmmjnpegb1.execute-api.us-east-2.amazonaws.com/default/yelp", json_new)
        r2 = requests.post("https://mslxpsw8vl.execute-api.us-east-2.amazonaws.com/default/lodging", json_new)
        r3 = requests.post("https://swda035v8d.execute-api.us-east-2.amazonaws.com/default/transport", json_new)
        


        for city in attributes_manager.session_attributes["cities"]:
            print(city)
        
        print(r.text)
        print(r1.text)
        print(r2.text)
        print(r3.text)
        
        
        
        flight_costs = []
        transport_costs = []
        transport_texts = []
        hotel_costs = []
        hotel_texts = []
        food_texts = []
        food_costs = []
        
        p_json = json.loads(r.text)
        for key in p_json.keys():
            key_json = p_json[key]
            flight_costs.append(key_json["average_cost"])
        
        p_json = json.loads(r3.text)
        for key in p_json.keys():
            cost = p_json[key]["transportation"][0]["cost"]
            text = p_json[key]["text"]
            transport_costs.append(cost)
            transport_texts.append(text)
        
        p_json = json.loads(r2.text)
        for key in p_json.keys():
            text = p_json[key]["text"]
            cost = p_json[key]["average_cost"]
            hotel_texts.append(text)
            hotel_costs.append(cost)
            
        p_json = json.loads(r1.text)
        for key in p_json.keys():
            text = p_json[key]["text"]
            cost = p_json[key]["average_cost"]
            food_texts.append(text)
            food_costs.append(cost)
        
        speak_output = ""
        for i in range(len(attributes_manager.session_attributes["cities"])):
            total_cost = flight_costs[i] + transport_costs[i] + hotel_costs[i] + food_costs[i]
            city = attributes_manager.session_attributes["cities"][i]
            if attributes_manager.session_attributes["cities"] < budget:
                speak_output += " I found a trip to {city} in your budget. The total cost is {total_cost}.".format(city=city, total_cost=total_cost) + hotel_texts[i] + " " + food_texts[i] + " " + transport_texts[i]
            else:
                speak_output += "I could not find any trips within your budget."
            
        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        

        return (
            handler_input.response_builder
                .speak(speak_output)
                #.ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        
        print(exception)
        
        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = CustomSkillBuilder(persistence_adapter=s3_adapter)

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GetCityIntentHandler())
sb.add_request_handler(GetMoreCitiesIntentHandler())
sb.add_request_handler(NoMoreCitiesIntentHandler())
sb.add_request_handler(GetVacationDaysIntentHandler())
sb.add_request_handler(GetBudgetIntentHandler())
sb.add_request_handler(SetBudgetIntentHandler())
sb.add_request_handler(CheckTripsIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()

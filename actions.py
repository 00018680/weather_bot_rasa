# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import json
import spacy
nlp = spacy.load("en_core_web_sm")

API_KEY = "b5e54fdebd2d45caaf890409241608"


def get_weather_data(place):
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={place}&aqi=no"
    response = requests.get(url=url).json()
    temp = response["current"]["temp_c"]
    condition = response["current"]["condition"]["text"]
    wind_mph = response["current"]["wind_mph"]
    humidity = response["current"]["humidity"]
    return {
        "temp": temp,
        'condition': condition,
        "wind_mph": wind_mph,
        "humidity": humidity
    }

class get_weather(Action):

    def name(self) -> Text:
        return "get_current_weather"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_input = tracker.latest_message['text']
        doc = nlp(user_input)
        city = None
        for ent in doc.ents:
            if ent.label_ == 'GPE':  # GPE stands for Geopolitical Entity (e.g., countries, cities)
                city = ent.text
                break
        if city:
            data = get_weather_data(city)
            temp = data["temp"]
            condition = data["condition"]
            wind_mph = data["wind_mph"]
            humidity = data["humidity"]
            text_message = (f"The weather in {city} is {condition}, and the temperature is {temp} Celcius."
                            f"Humidity level is {humidity}, and there is also wind which blows at around {wind_mph} meters per hour")


            dispatcher.utter_message(text=text_message)
        else:
            dispatcher.utter_message(text="I couldn't find a city in your message. Please specify a city.")


class ActionDefaultFallback(Action):

    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="I did not get what you mean. Can you specify?")
        return []

import json
import random
import math
import urllib.request
import boto3

import allrecipes as ar

######################################
#          Global Variables          #
######################################
# Amazon Dynmo Database Initialization
dynamodb = boto3.resource('dynamodb')
ChefAlexaTable = dynamodb.Table('ChefAlexa')
#################

# Other Global Variables

phase = 0

foodName = [None]


# foodNum = [None]


######################################

######################################
#          General Functions         #
######################################
# Updates Users Data from Website
def updateUsers():
    global users

    with urllib.request.urlopen("https://dralexa2.pythonanywhere.com/") as url:
        users = json.loads(url.read().decode())
    return users


# Snellen Exam Dynmo Database Update
def databaseUpdate():
    ChefAlexaTable.put_item(
        Item={
            'ID': 0,
            'Ingredient': foodName,
        }
    )
    return


######################################
#           Alexa Handlers           #
######################################
##############################
# Builders
##############################


def build_SSML(output):
    return {
        'response': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': '<speak>' + output + '</speak>'
            },
            'card': {
                'type': 'Simple',
                'title': "SessionSpeechlet - Ingredients ",
                'content': "SessionSpeechlet - " + str(foodName[0])
            },
            'reprompt': {
                'outputSpeech': {
                    'type': 'SSML',
                    'ssml': '<speak>' + output + '</speak>'
                }
            },
            'shouldEndSession': False,
            'session': {
                'new': True
            }
        }
    }


def get_perm():
    # access_token = event['context']['System']['apiAccessToken']
    # email = str(access_token) + '/v2/accounts/~current/settings/Profile.email'
    return {
        "response": {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': '<speak> Please grant permissions in the alexa app in order to get your name and email.</speak>'
            },
            "card": {
                "type": "AskForPermissionsConsent",
                "permissions": [
                    "alexa::profile:name:read",
                    "alexa::profile:email:read"
                ]
            }
        }
    }


##############################
# Custom Intents
##############################

# Adds food item to the list
def addItem(event, context):
    global foodName
    # global foodNum

    foodItem = event['request']['intent']['slots']['Food']['value']

    if foodName[0] == None:
        foodName[0] = foodItem
    else:
        foodName.append(foodItem)

    # try:
    #     foodNumber = event['request']['intent']['slots']['Number']['value']
    #     if foodNum[0] == None:
    #         foodNum[0] = foodNumber
    #     else:
    #         foodNum.append(foodNumber)
    # except:
    #     if foodNum[0] == None:
    #         foodNum[0] = 1
    #     else:
    #         foodNum.append(1)

    return build_SSML("Added!")


# When the user finished ingredients list
def Done(event, context):
    databaseUpdate()
    # ans = ""
    # for i in range(len(foodName)):
    #     if(i == len(foodName)-1):
    #         ans += "and "
    #     ans += str(foodNum[i]) + " " + str(foodName[i])
    #     if(i != len(foodName)-1):
    #         ans += ", "
    #     else:
    #         ans += " "
    return Calculate()
    # return build_SSML("Ok ingredients added, Checking recipe for %s" % foodName)


inst = [None]


def Calculate():
    global inst
    # keyword = input('what would you like to eat: ')
    # inc_i = 0
    # included = []
    # inc_input = int(input('how many items do you want to include (max 3): '))
    # while inc_i < inc_input:
    #     inc_ingr = input("ingredient(s) to include: ")
    #     included.append(inc_ingr)
    #     inc_i +=1

    # exc_i = 0
    # excluded = []
    # exc_input = int(input('how many items do you want to not include (max 3): '))
    # while exc_i < exc_input:
    #     exc_ingr = input("ingredient(s) to not include: ")
    #     excluded.append(exc_ingr)
    #     exc_i +=1
    # Search :
    query_options = {
        "wt": "pork curry",  # Query keywords
        "ingIncl": "olives",  # 'Must be included' ingrdients (optional)
        "ingExcl": "onions salad",  # 'Must not be included' ingredients (optional)
        "sort": "re"  # Sorting options : 're' for relevance, 'ra' for rating, 'p' for popular (optional)
    }
    query_result = asearch(query_options)
    return build_SSML("works")


# Resets Alexa's attention span
def Wait(event, context):
    return statement("Wait", "Please Pick a food item.")


def Error(currentPhase, text):
    if currentPhase == 0:
        return statement("Error", text + "I am sorry, there seems to be a problem, please select a food item.")


##############################
# Required Intents
##############################
def cancel_intent():
    return statement("CancelIntent",
                     "You want to cancel")  # don't use CancelIntent as title it causes code reference error during certification


def help_intent():
    return statement("HelpIntent", "You want help")  # same here don't use CancelIntent


def stop_intent():
    return statement("StopIntent", "You want to stop")  # here also don't use StopIntent


##############################
# On Launch
##############################
def on_launch(event, context):
    # Initialize Values Here
    # ChefAlexaTable.put_item(
    #     Item={
    #         'ID': 0,
    #         'Ingredient': []
    #     }
    # )
    # build_SSML(str(req_email))
    # get_perm()
    # access_token= event['context']['System']['user']['accessToken']
    return build_SSML("Welcome to Chef Alexa, What's in your fridge?")


def on_Exit(event, context):
    return build_SSML("Thanks for choosing Alexa Chef")


##############################
# Routing
##############################
def intent_router(event, context):
    intent = event['request']['intent']['name']

    # Custom Intents
    # Intent that is always accessible after phase 1 is completed
    if intent == "ingredients":
        return addItem(event, context)
    elif intent == "done":
        return Done(event, context)
    elif intent == "CancelIntent":
        return cancel_intent()
    elif intent == "HelpIntent":
        return help_intent()
    elif intent == "StopIntent":
        return stop_intent()


##############################
# Program Entry
##############################
def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event, context)
    elif event['request']['type'] == "IntentRequest":
        return intent_router(event, context)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_Exit(event, context)
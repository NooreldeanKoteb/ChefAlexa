import json
import random
import math
import urllib.request
import boto3

######################################
#          Global Variables          #
######################################
# Amazon Dynmo Database Initialization
dynamodb = boto3.resource('dynamodb')
ChefAlexaTable = dynamodb.Table('ChefAlexa')
#################

phase = 0

######################################
#          General Functions         #
######################################
# Updates Users Data from Website
def updateUsers():
    global users

    with urllib.request.urlopen("https://dralexa2.pythonanywhere.com/patientInfo/") as url:
        users = json.loads(url.read().decode())
    return users


# Snellen Exam Dynmo Database Update
def databaseUpdate():
    ChefAlexaTable.put_item(
        Item={
            'ID': 0,
        }
    )
    return


######################################
#           Alexa Handlers           #
######################################
##############################
# Builders
##############################

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': output
            },
            'card': {
                'type': 'Simple',
                'title': "SessionSpeechlet - " + title,
                'content': "SessionSpeechlet - " + output
            },
            'reprompt': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': reprompt_text
                }
            },
            'shouldEndSession': should_end_session
        }
    }


def build_SSML(greeting, output, should_end_session, new_session):
    return {
        'response': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': '<speak> <p>' + greeting + '</p> <prosody rate="90%"><p>' + output + '</p> <audio src = "https://emptysound.s3.amazonaws.com/EmptySound.mp3" /> </prosody> </speak>'
            },
            'card': {
                'type': 'Simple',
                'title': "SessionSpeechlet - " + greeting,
                'content': "SessionSpeechlet - " + output
            },
            'reprompt': {
                'outputSpeech': {
                    'type': 'SSML',
                    'ssml': '<speak> <p>' + greeting + '</p> <prosody rate="85%"><p>' + output + '</p> <audio src = "https://emptysound.s3.amazonaws.com/EmptySound.mp3" /> </prosody> </speak>'
                }
            },
            'shouldEndSession': should_end_session,
            'session': {
                'new': new_session
            }
        }
    }


def build_PlainSpeech(body):
    speech = {}
    speech['type'] = 'PlainText'
    speech['text'] = body
    return speech


def build_response(message, session_attributes={}):
    response = {}
    response['version'] = '1.0'
    response['sessionAttributes'] = session_attributes
    response['response'] = message
    return response


def build_SimpleCard(title, body):
    card = {}
    card['type'] = 'Simple'
    card['title'] = title
    card['content'] = body
    return card


##############################
# Responses
##############################

# deals with conversation between user and Alexa
def conversation(title, body, session_attributes):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = False
    return build_response(speechlet, session_attributes=session_attributes)


# is a simple one way statement expecting no input from user
def statement(title, body):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = False
    # return build_response(speechlet)
    return build_SSML("", body, False, False)


# this creats a dialog message which is sent to build_response
def continue_dialog():
    message = {}
    message['shouldEndSession'] = False
    message['directives'] = [{'type': 'Dialog.Delegate'}]
    return build_response(message)


##############################
# Custom Intents
##############################


# Resets Alexa's attention span
def Wait(event, context):
    return statement("Wait", "Please read the letters on the screen!")


def Error(currentPhase, text):
    if currentPhase == 0:
        return statement("Error", text + "Please select an exam Type. Would you like a visual Test or a prescription Test?")


##############################
# Required Intents
##############################
def cancel_intent():
    return statement("CancelIntent", "You want to cancel")  # don't use CancelIntent as title it causes code reference error during certification

def help_intent():
    return statement("HelpIntent", "You want help")  # same here don't use CancelIntent


def stop_intent():
    return statement("StopIntent", "You want to stop")  # here also don't use StopIntent


##############################
# On Launch
##############################
def on_launch(event, context):
    #Initialize Values Here

        #INitializations
    return build_SSML("Welcome To The Snellen Exam", "would you like to run a visual exam or a prescription exam",
                      False, True)


def on_Exit(event, context):
    return build_SSML("Greetings", "Thank you for choosing Snellen Exam, Bye Bye", "Bye", True, False)


##############################
# Routing
##############################
def intent_router(event, context):
    intent = event['request']['intent']['name']

    # Custom Intents
    # Intent that is always accessible after phase 1 is completed
    if phase >= 0:
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

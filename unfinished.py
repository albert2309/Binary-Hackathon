import json
import dateutil.parser
import datetime
import time
import os
import math
import random
import logging


def lambda_handler(event, context):
    # By default, treat the user request as coming from the America/New_York time zone.
    return dispatch(event)


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """
    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'SearchContact':
        return searchAddress(intent_request)
    raise Exception('Intent with name ' + intent_name + ' not supported')


def searchAddress(intent_request):
    location = intent_request['currentIntent']['slots']['whatCity']
    source = intent_request['invocationSource']
    output_session_attributes = intent_request['sessionAttributes'] if intent_request[
                                                                           'sessionAttributes'] is not None else {}

    if source == 'DialogCodeHook':
        if not location:
            return elicit_slot(
                output_session_attributes,
                intent_request['currentIntent']['name'],
                intent_request['currentIntent']['slots'],
                'BranchLocationInput',
                {'contentType': 'PlainText', 'content': 'What city are you currently in?'},
                build_response_card(
                    'Which city', 'What city are you currently in?',
                    build_options('whatCity', location)
                )
            )
        if not whatMedicine:
            return elicit_slot(
                output_session_attributes,
                intent_request['currentIntent']['name'],
                intent_request['currentIntent']['slots'],
                'BranchLocationInput',
                {'contentType': 'PlainText', 'content': 'Do you know which medicine you want?'},
                build_response_card(
                    'Self-diagnosis', 'Do you know which medicine you want?',
                    build_options('whatMedicine', location)
                )
            )
        if whatMedicine == 'yes':
            if not typeOfSick:
                return elicit_slot(
                    output_session_attributes,
                    intent_request['currentIntent']['name'],
                    intent_request['currentIntent']['slots'],
                    'BranchLocationInput',
                    {'contentType': 'PlainText', 'content': 'What symptoms are you experiencing?'},
                    build_response_card(
                        'Self-diagnosis', 'What symptoms are you experiencing?',
                        build_options('whatMedicine', location)
                    )
                )
            if typeOfSick == 'Nausea' and whatCity == 'Jakarta':
                return elicit_slot(
                    output_session_attributes,
                    intent_request['currentIntent']['name'],
                    intent_request['currentIntent']['slots'],
                    'BranchLocationInput',
                    {'contentType': 'PlainText', 'content': 'Okay let me translate to Indonesia: \n "Saya butuh obat'},
                    build_response_card(
                        'Self-diagnosis', 'What symptoms are you experiencing?',
                        build_options('whatMedicine', location)
                    )
                )


def build_options(slot, location):
    """
    Build a list of potential options for a given slot, to be used in responseCard generation.
    """
    if slot == 'whatCity':
        return [
            {'text': 'Jakarta', 'value': 'Jakarta'},
            {'text': 'Tokyo', 'value': 'Tokyo'}
        ]
    elif slot == 'whatMedicine':
        return [
            {'text': 'yes', 'value': 'yes'},
            {'text': 'no', 'value': 'no'}
        ]
    elif slot == 'typeOfSick':
        return [
            {'text': 'Diziness', 'value': 'Diziness'},
            {'text': 'Nausea', 'value': 'Nausea'},
            {'text': 'Stomachache', 'value': 'Stomachache'}
        ]
    elif


""" --- Helpers to build responses which match the structure of the necessary dialog actions --- """


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message, response_card):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message,
            'responseCard': response_card
        }
    }


def confirm_intent(session_attributes, intent_name, slots, message, response_card):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ConfirmIntent',
            'intentName': intent_name,
            'slots': slots,
            'message': message,
            'responseCard': response_card
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


def build_response_card(title, subtitle, options):
    """
    Build a responseCard with a title, subtitle, and an optional set of options which should be displayed as buttons.
    """
    buttons = None
    if options is not None:
        buttons = []
        for i in range(min(5, len(options))):
            buttons.append(options[i])

    return {
        'contentType': 'application/vnd.amazonaws.card.generic',
        'version': 1,
        'genericAttachments': [{
            'title': title,
            'subTitle': subtitle,
            'buttons': buttons
        }]
    }


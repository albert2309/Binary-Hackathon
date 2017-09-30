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
    location = intent_request['currentIntent']['slots']['BranchLocationInput']
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
                {'contentType': 'PlainText', 'content': 'What type of location would you like see?'},
                build_response_card(
                    'Which location', 'What type of location would you like see?',
                    build_options('BranchLocationInput', location)
                )
            )
        elif location:

            if location == 'Malta':
                return close(
                    output_session_attributes,
                    'Fulfilled',
                    {
                        'contentType': 'PlainText',
                        'content': 'Binary (Europe) Ltd & Binary Investments (Europe) Ltd,\n Mompalao Building, Suite 2, Tower Road, Msida MSD1825\n'
                    }
                )
            elif location == 'Japan':
                return close(
                    output_session_attributes,
                    'Fulfilled',
                    {
                        'contentType': 'PlainText',
                        'content': 'Binary KK, Hiroo Miyata Bldg 3F, 9-16, Hiroo 1-chome,\n Shibuya-ku, Tokyo 150-0012, Japan'
                    }
                )
            elif 'Malaysia' in location:

                if location == 'Malaysia, Cyberjaya':
                    return close(
                        output_session_attributes,
                        'Fulfilled',
                        {
                            'contentType': 'PlainText',
                            'content': 'Binary Group Services Sdn Bhd,\n C-13-02, iTech Tower, Jalan Impact,\n Cyber 6, 63000 Cyberjaya,\n Selangor Darul Ehsan'
                        }
                    )
                elif location == 'Malaysia, Kuala Lumpur':
                    return close(
                        output_session_attributes,
                        'Fulfilled',
                        {
                            'contentType': 'PlainText',
                            'content': 'Binary Group Services Sdn Bhd,\n30-10, Q Sentral,  Jalan Stesen Sentral 2,\n 50470 Kuala Lumpur'
                        }
                    )
                else:
                    return elicit_slot(
                        output_session_attributes,
                        intent_request['currentIntent']['name'],
                        intent_request['currentIntent']['slots'],
                        'BranchLocationInput',
                        {'contentType': 'PlainText', 'content': 'What type of region would you like see?'},
                        build_response_card(
                            'Which location', 'What type of location would you like see?',
                            build_options('MalaysiaInput', location)
                        )
                    )


def build_options(slot, location):
    """
    Build a list of potential options for a given slot, to be used in responseCard generation.
    """
    if slot == 'BranchLocationInput':
        return [
            {'text': 'Malta', 'value': 'Malta'},
            {'text': 'Japan', 'value': 'Japan'},
            {'text': 'Malaysia', 'value': 'Malaysia'}
        ]
    elif slot == 'MalaysiaInput':
        return [
            {'text': 'Malaysia, Cyberjaya', 'value': 'Malaysia, Cyberjaya'},
            {'text': 'Malaysia, Kuala Lumpur', 'value': 'Malaysia, Kuala Lumpur'}
        ]


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


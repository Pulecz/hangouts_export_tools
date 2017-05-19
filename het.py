#!/usr/bin/env python
import json

hangouts_export_json = 'Setkání.json'
debug = False

def load_json(json_file):
    with open(json_file) as json_f:
        data = json.loads(json_f.read())
    return data

def parse_messages(data):
    """
    returns dict with keys based on people_in_conversation

    change number in target to select person, in my case its index 4
    """
    target = data['conversation_state'][4]['conversation_state']['event']
    people_in_conversation = {
        "person_A": "numeric id of len of 21",
        "person_B": "numeric id of len of 21"
        }
    result = {}
    #TODO fix, index is only for saving purposes to result
    for index, event in enumerate(target):

        #get segment from event
        try:
            if event.get("hangout_event"):
                #not much we can do with hangout_event, only report when they happened
                if debug: print('hangout event')
                continue
            if event["chat_message"]["message_content"].get("attachment") is not None:
                #ignoring attachmenets
                if debug: print('got attachment')
                continue
            else:
                segment = event["chat_message"]["message_content"]["segment"][0]
        except KeyError as e:
            print(e)
            print('ERROR: Please investigate:\n', json.dumps(event))
            input()

        #got segment, continue
        if segment["type"] == 'TEXT':
            for person, gaia_id in people_in_conversation.items():
                if event["sender_id"]["gaia_id"] == gaia_id:
                    if result.get(person) is None: #if the result does not have this person specified yet
                        #create key for the person
                        result[person] = {}
                    result[person][index] = segment["text"]
                    if debug: print(person, 'said', segment["text"])

        elif segment["type"] == 'LINK': continue #skipping links
        elif segment["type"] == 'LINE_BREAK': continue #interesting, just one instance of this
        else:
            print('WARNING: Unhandled segment, please handle:\n',json.dumps(segment))
            input()
        if debug:
            print(json.dumps(event))
            input()
    return result

def main():
    input_data = load_json(hangouts_export_json)
    out = parse_messages(input_data)

if __name__ == '__main__':
    input_data = load_json(hangouts_export_json)
    out = parse_messages(input_data)

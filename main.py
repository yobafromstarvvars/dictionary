import json
import urllib.request

"""
definition
image
sound
synonyms
antonyms
sentences
collocations
how popular is the word
category (tag)
"""

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

params = {
    "note": {
        "deckName": "Cambridge",
        "modelName": "Basic",
        "fields": {
            "Front": "front content",
            "Back": "back content"
        }
    },
    "tags": ["idiom",]
}

note = {
    "deckName": "Cambridge",
        "modelName": "Basic",
        "fields": {
            "Front": "Hello world",
            "Back": "back content"
        }
}

tags = ["idiom",]


invoke('addNote', note=note, tags=tags)
# result = invoke('deckNames')
# print('got list of decks: {}'.format(result))
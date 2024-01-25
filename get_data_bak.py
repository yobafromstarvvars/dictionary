import requests
import pprint
import json
import sys

mw_key_1 = "eb51743f-c840-4b3f-bbe5-d3c42c4e8883" # Learner's dictionary
# mw_key_2 = "63aebef2-b89f-4040-8124-c723ec526a96" # Intermediate Thesaurus

# res = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/hello")
url = "https://dictionaryapi.com/api/v3/references/learners/json/"
audio_url = "https://media.merriam-webster.com/audio/prons/[language_code]/[country_code]/[format]/[subdirectory]/[base filename].[format]"


def get_definition(search_word):
    # Query info set up

    params = {
        "key": mw_key_1
    }
    # Build a query
    query = url + search_word + "?"
    for key, value in params.items():
        query += f"{key}={value}"

    res = requests.get(query)

    with open("res.json", "w") as f:
        json.dump(res.json(), f)

    return res.json()

# pprint.pprint(get_definition("traffic")[0]['def'])
# sys.exit()

# ['{bc} all the vehicles driving along a certain road or in a certain area',
#  '{bc} the movement of airplanes, ships, etc., along routes',
#  '{bc} the amount of people who pass through a certain place or travel in a '
#  'certain way']


# for l in res.json():
#     print(l)
#     print('\n\n\n')
# print(len(res.json()))

# with open("res.json", "w") as f:
#     json.dump(res.json(), f)

###########################################################
word_data = ""
with open('res.json') as f:
  word_data = json.load(f)
###########################################################

# pprint.pprint(word_data[0]['meta'])

search_word = "hit"
word_data = get_definition(search_word)

# shot defenition
description = {
    "word": "",
    "part_of_speech": "",
    "ipa": "",
    "image": "",
    "popularity": "",
    "collocations": "",
    "definitions": [{
        "text": "",
        "examples": [],
        "synonyms": [],
        "antonyms": [],
        "is_singular": True,
        "is_count": True,
        "additional": "", # transitive or not, not used somewhre
        "label": "", # informal, written, formal etc.
    }, ],
}
# "search_word": {"sn": word, "fields": []}
failed_to_add = {} 

card = {
    "front": "",
    "back": "",
}

# One definition (sense) in a card
# text, examples
definition = ""



if word_data:
    if type(word_data[0]) == dict:
        # At least one definition found
        
        for word in word_data:
            # print("\n\n\n\n\n\n")
            # print(word)
            # sys.exit()
            description["word"] = word['meta']['app-shortdef']['hw']
            description["part_of_speech"] = word['meta']['app-shortdef']['fl']
            

            if "ipa" in word["hwi"]["prs"][0]:
                # If 
                description["ipa"] = word["hwi"]["prs"][0]["ipa"]

            
 
            for sseq in word["def"]:
                
                for sense in sseq["sseq"]:

                    for sense_type in sense:

                        # it can be sen or sense

                        if sense_type[0] == 'sen':

                            # print(sense_type[1])
                            # print(sense_type)
                            # if "sgram" in sense_type[1]:
                            #     print(sense_type[1]["sgram"])
                            # main_sense_num = sense_type[1]["sn"]
                            pass

                        elif sense_type[0] == 'sense':
                            
                            print(sense_type)

                            # Definition 
                            if "dt" in sense_type[1]:

                                # Get text
                                if i[0] == "text":
                                    description["definition"].append(i[1])
                                else:
                                    failed_to_add.setdefault(description["word"], [])
                                    failed_to_add[description["word"]].append("text")


                                for i in sense_type[1]["dt"]:
                                    
                                    
                                    if i[0] == "vis":
                                        description["examples"].append
                            
                                # if "text" in sense_type[1]["dt"]:
                                #     description["definition"] = sense_type[1]["dt"]["text"]

                            # if "lbs" in sense_type[1]:
                            #     # Additional info such as "not used in progressive tenses"
                            #     pass

                            # if "sls" in sense_type[1]:
                            #     # Informal / formal / written / technical / etc.
                            #     pass
                            
                            

                            # if "vis" in sense_type[1]:
                            #     pass

                            # if "wsgram" in sense_type[1]:
                            #     pass
                            

                            # definition = sense_type[1]["dt"][0][1]
                            # # pprint.pprint(sense_type[1]["dt"][1][1])
    
                            # pprint.pprint(sense_type[1]["dt"][1])
                            # for vis in sense_type[1]["dt"][1]:
                            #     pprint.pprint(type(vis))

                            # examples = []
                            # for example in sense_type[1]["dt"][1][1]:
                            #     for e in example:
                            #         examples.append(e['t'])
                            # examples = [e for e in sense_type[1]["dt"][1][1]] # Create a list of examples
                            # pprint.pprint(examples)

                    # add_info = sense[0][1]["lbs"]
                    
                    
                    # examples = sense[0][1]["dt"]
                    print("\n"*5)
                pprint.pprint(description["definition"])
                sys.exit()
                print(str(index) + ": ", end='')
                print(definition)
                # print(definition['sseq'])
                
            sys.exit()
    else:
       print("Maybe you meant:")
       for word in word_data:
          print(word)
else:
   print("Not found")


# head_word = word_data[0]['hwi']['hw']


# synonyms = word_data[0]["syn_list"]
# definition = "" # def also has his own: plural or singular, popularity
# antonyms = ""

"""
definition:
    definition
    count / uncount
    examples
    sysnonyms
    antonyms
    popu
"""

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
pronunciation (american)
plural or singular
countable or uncountable
"""

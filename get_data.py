import requests
import pprint
import json
import sys
from word_list import word_list
from jinja2 import Template
from config import *


def get_word_data(search_word, params={"key": learners_key}, api_name=learners_api_name):
    # Get word data from a dictionary with api

    # Build a query
    query = "/".join([api_url, api_name, "json", search_word]) + "?"
    for key, value in params.items():
        query += f"{key}={value}"

    # Get the json data
    res = requests.get(query)

    return res.json()


def get_word_data_fake(filename):
    word_data = ""
    with open(filename) as f:
        word_data = json.load(f)
    return word_data


def write_word_data(filename, word_data):
    with open(filename, "w") as f:
        json.dump(word_data, f)


log_info = {
    "no_def_tag": {
        "count": 0,
        "entries": []
    },
    "failed": 0,
    "total": 0,

}



for entry in word_list:
    l.info(f"Word in progress: {entry[0]}")

    # Prepare dictionary to store all the necessary word data
    description = {
        "word": "",
        "part_of_speech": "",
        "ipa": "",
        "images": [],
        "collocations": "",
        "definitions": [{
            "text": "",
            "popularity": "",
            "examples": [],
            "synonyms": [],
            "antonyms": [],
            "is_singular": True,
            "is_count": True,
            "grammar_info": [],  # transitive or not, not used somewhre
            "label": "",  # informal, written, formal etc.
        }, ],
    }

    # Get word data from dictionary api
    # word_data = get_word_data(entry[0])

    word_data = get_word_data_fake("learners_get.json")
    

    # Go through api data and get necessary data 
    if word_data:
        if type(word_data[0]) == dict:
            
            # At least one definition found
            
            dl.debug(f"word data length: {len(word_data)}")

            for word in word_data:
                # description["word"] = word['meta']['app-shortdef']['hw']
                # description["part_of_speech"] = word['meta']['app-shortdef']['fl']
                # description["definitions"] = word['meta']['app-shortdef']['def']
                # dl.debug(word["hwi"])

                description["word"] = word["hwi"]["hw"]

                try:
                    pronunciation = word["hwi"]["prs"]
                    description["ipa"] = pronunciation[0]["ipa"]
                except:
                    l.debug(f"{word['hwi']['hw']}: ipa not found")

                # Some words don't have def
                if "def" not in word:
                    l.debug(f"{word['hwi']['hw']}: 'def' tag not found")
                    continue

                for sseq in word["def"]:

                    dl.debug(sseq)

                    for definition in sseq["sseq"]:

                        dl.debug(definition)

                        if "vd" in definition:
                            description["grammar_info"].append(definition["vd"])

                        for sense_type in definition:

                            text = ""
                            examples = ""

                            # it can be sen or sense

                            if sense_type[0] == 'sen':

                                # print(sense_type[1])
                                # print(sense_type)
                                # if "sgram" in sense_type[1]:
                                #     print(sense_type[1]["sgram"])
                                # main_sense_num = sense_type[1]["sn"]
                                pass

                            elif sense_type[0] == 'sense':

                                # Definition
                                if "dt" in sense_type[1]:

                                    for i in sense_type[1]["dt"]:
                                        pass
                                        # # Get text
                                        # if i[0] == "text":
                                        #     description["definition"].append(i[1])
                                        # else:
                                        #     failed_to_add.setdefault(description["word"], [])
                                        #     failed_to_add[description["word"]].append("text")

                                        # if i[0] == "vis":
                                        #     description["examples"].append

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
                    # pprint.pprint(description["definition"])
                    

                    # print(str(index) + ": ", end='')
                    # print(definition)
                    # print(definition['sseq'])

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

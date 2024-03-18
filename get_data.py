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
    # Open and read a file where data from a real response is stored

    word_data = ""
    with open(filename) as f:
        word_data = json.load(f)
    return word_data


def write_word_data(filename, word_data):
    with open(filename, "w") as f:
        json.dump(word_data, f)


def t_create_json(word):
    # Create json file with word description from THESAURUS dictionary

    word_data = get_word_data(word, {"key": ithesaurus_key}, api_name=thesaurus_api_name)
    write_word_data(f"thesaurus_{word}.json", word_data)


def l_create_json(word):
    # Create json file with word description from LEARNERS dictionary

    word_data = get_word_data(word)
    write_word_data(f"learners_{word}.json", word_data)





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
        "is_count": True,
        "definitions": [{
            "number": "",
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

    word_data = get_word_data_fake("thesaurus_get.json")
    

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

                # Some words don't have def. Don't add them
                if "def" not in word:
                    l.debug(f"{word['hwi']['hw']}: 'def' tag not found")
                    continue

                description["word"] = word["hwi"]["hw"]

                if "gram" in word:
                    description["is_count"] = word["gram"]

                try:
                    pronunciation = word["hwi"]["prs"]
                    description["ipa"] = pronunciation[0]["ipa"]
                except:
                    l.debug(f"{word['hwi']['hw']}: ipa not found")

                for sseq in word["def"]:

                    dl.debug(sseq)

                    for definition in sseq["sseq"]:

                        dl.debug(definition)

                        # One definition has several senses
                        for sense in definition:

                            word_definition = {
                                "popularity": "",
                                "number": "",
                                "text": "",
                                "examples": [],
                                "synonyms": [],
                                "antonyms": [],
                                "is_singular": True,
                                "is_count": True,
                                "grammar_info": [],  # transitive or not, not used somewhre
                                "label": "",  # informal, written, formal etc.
                            }

                            # Verb divider (grammar): transitive, intransitive
                            if "vd" in definition:
                                word_definition["grammar_info"].append(definition["vd"])

                            dl.debug(sense)

                            # It can be sen or sense
                            sense_type = sense[0]
                            sense_data = sense[1]

                            text = ""
                            examples = ""

                            if sense_type == 'sen':

                                # print(sense[1])
                                # print(sense)
                                # if "sgram" in sense[1]:
                                #     print(sense[1]["sgram"])
                                # main_sense_num = sense[1]["sn"]
                                word_definition["number"] = sense_data["sn"]
                                

                            elif sense_type == 'sense':

                                # Definition
                                # if "dt" in sense[1]:
                                sense_body = sense_data["dt"]

                                
                                #
                                # Add synonyms and antonyms. They have the same structure, so we can use one script
                                #
                                synonym_key_name = ["syn_list", "sim_list", "rel_list"]  # names of keys of synonyms in api json
                                antonym_key_name = ["ant_list", "near_list"]  # names of keys of antonyms in api json
                                for key in synonym_key_name + antonym_key_name:
                                    if key in sense_data:
                                        dl.debug(sense_data[key])
                                        # sense_data[i] is [[{'wd': 'learn'}, {'wd': 'master'}, {'wd': 'pick up'}]]
                                        for rel_word_group in sense_data[key]:  
                                            # rel_word_group is a list of dicts where 2nd element is the word
                                            # rel_word_group is [{'wd': 'learn'}, {'wd': 'master'}, {'wd': 'pick up'}]
                                            dl.debug(rel_word_group)

                                            # List that will be added to word definition 
                                            # (first, find all the words, second, add them to the word_definition)
                                            rel_words = []
                                            for rel_word in rel_word_group:
                                                # rel_word is {'wd': 'learn'}
                                                rel_words.append(rel_word["wd"])
                                            if key in synonym_key_name:
                                                # If the words are synonyms, add them to 'word_definition' dict
                                                word_definition["synonyms"] += rel_words
                                            else:
                                                word_definition["antonyms"] += rel_words

                                # # Synonym list 
                                # if "rel_list" in sense_data:
                                #     for synonym_group in sense_data["rel_list"]:
                                #         # List that will be added to word definition
                                #         synonyms = []
                                #         for synonym in synonym_group:
                                #             synonyms.append(synonym["wd"])
                                #         word_definition["synonyms"].append(synonyms)

                                # # Synonym list 
                                # if "rel_list" in sense_data:
                                #     for synonym_group in sense_data["rel_list"]:
                                #         # List that will be added to word definition
                                #         synonyms = []
                                #         for synonym in synonym_group:
                                #             synonyms.append(synonym["wd"])
                                #         word_definition["synonyms"].append(synonyms)


                                if "sn" in sense_data:    
                                    word_definition["number"] = sense_data["sn"]
                                    

                                if "sgram" in sense_data:
                                    word_definition["label"] = sense_data["sgram"]
                                
            
                                for info in sense_body:

                                    info_type = info[0]
                                    info_data = info[1]

                                    dl.debug(info)

                                    # Definition text
                                    if info_type == "text":
                                        
                                        dl.debug(info_data)

                                        word_definition["text"] = info_data


                                    # Examples
                                    elif info_type == "vis":
                                        
                                        for example in info_data:
                                            dl.debug(example)
                                            word_definition["examples"] = example["t"]

                                    elif info_type == "uns":
                                        pass

                                    elif info_type == "wsgram":
                                        dl.debug(info_data)
                                        word_definition["is_count"] = info_data
                                        word_definition["grammar_info"].append(info_data)
                                    
                                    # # Get text
                                    # if i[0] == "text":
                                    #     description["definition"].append(i[1])
                                    # else:
                                    #     failed_to_add.setdefault(description["word"], [])
                                    #     failed_to_add[description["word"]].append("text")

                                    # if i[0] == "vis":
                                    #     description["examples"].append

                                    # if "text" in sense[1]["dt"]:
                                    #     description["definition"] = sense[1]["dt"]["text"]

                                # if "lbs" in sense[1]:
                                #     # Additional info such as "not used in progressive tenses"
                                #     pass

                                # if "sls" in sense[1]:
                                #     # Informal / formal / written / technical / etc.
                                #     pass

                                # if "vis" in sense[1]:
                                #     pass

                                # if "wsgram" in sense[1]:
                                #     pass

                                # definition = sense[1]["dt"][0][1]
                                # # pprint.pprint(sense[1]["dt"][1][1])

                                # pprint.pprint(sense[1]["dt"][1])
                                # for vis in sense[1]["dt"][1]:
                                #     pprint.pprint(type(vis))

                                # examples = []
                                # for example in sense[1]["dt"][1][1]:
                                #     for e in example:
                                #         examples.append(e['t'])
                                # examples = [e for e in sense[1]["dt"][1][1]] # Create a list of examples
                                # pprint.pprint(examples)
                        pprint.pprint(word_definition)
                        sys.exit()
                        print()
                        print()

                        # add_info = sense[0][1]["lbs"]

                        # examples = sense[0][1]["dt"]
                        # print("\n"*5)
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

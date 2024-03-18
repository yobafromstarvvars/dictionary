import logging


learners_key = "eb51743f-c840-4b3f-bbe5-d3c42c4e8883" # Learner's dictionary
ithesaurus_key = "63aebef2-b89f-4040-8124-c723ec526a96" # Intermediate Thesaurus

# Words that is in the api url
learners_api_name = "learners"  
thesaurus_api_name = "ithesaurus"

# res = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/hello")
api_url = "https://dictionaryapi.com/api/v3/references"
audio_url = "https://media.merriam-webster.com/audio/prons/[language_code]/[country_code]/[format]/[subdirectory]/[base filename].[format]"
dict_url = "https://www.britannica.com/dictionary/"



# logging.basicConfig(filemode="w", filename="log.log", format="[%(asctime)s - %(name)s - %(levelname)s] %(message)s", level=logging.DEBUG, datefmt="%d/%m/%Y %H:%m:%S")
# logging.setLevel(logging.DEBUG)

def setup_logger(logger_name, log_file, level=logging.DEBUG):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s(%(lineno)d)] %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    # streamHandler.setFormatter(formatter)
    l.setLevel(level)
    l.addHandler(fileHandler)
    # l.addHandler(streamHandler)    


setup_logger('data_logger', "data_logger.log")
setup_logger('logger', "logger.log")
dl = logging.getLogger('data_logger')
l = logging.getLogger('logger')





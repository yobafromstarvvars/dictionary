from bs4 import BeautifulSoup
import requests
import sys

proxies = {
    # 'http': 'http://35.225.16.82:2387',
    'https': 'http://35.225.16.82:2387',
}

dict_page = requests.get("https://www.ldoceonline.com/dictionary/be-loath-to-do-something", proxies=proxies)
sys.exit()

with open("longman_entry.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

soup = BeautifulSoup("<html>a web page</html>", 'html.parser')
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse



def get_request(URL,headers):
    response = requests.get(URL, headers=headers)
    response.raise_for_status()  
    soup    = BeautifulSoup(response.text, "html.parser")
    return soup


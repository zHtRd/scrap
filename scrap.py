# Imports
import requests
from bs4 import BeautifulSoup

# Variables
baseUrl = ''
uri = ''

# HTTP GET sur URL souhaité
response = requests.get(baseUrl)
print(response)
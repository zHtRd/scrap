# Imports
import requests
from bs4 import BeautifulSoup

# Variables
baseUrl = 'https://www.studyrama.com'
uri = ''
response = requests.get(baseUrl)

# Réponse 200 Serveur
if response.ok:
    # Récupération page source
    swoup = BeautifulSoup(response.text, 'html.parser')
    # Get première balise <ul>...</ul>
    ul = swoup.find("ul")
    # ul = swoup.find("ul", {"class": "results"})
    # uls = swoup.findAll("ul",  {"class": "results"})

    lis = ul.findAll("li")
    for li in lis:
        a = li.find("a")
        print(a["href"])
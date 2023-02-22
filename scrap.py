# Imports
import requests
from bs4 import BeautifulSoup

# Variables
baseUrl = 'https://www.allocine.fr'
cineUri = '/film/'
aucineUri = '/film/aucinema/?page='


# HTTP GET sur URL souhaité
page = 1
response = requests.get(baseUrl + aucineUri + str(page))
oldUrl = ""

while response.ok and response.url != oldUrl:
    swoup = BeautifulSoup(response.text, 'html.parser')
    
    divs = swoup.findAll("div", {"class": "card entity-card entity-card-list cf"})
    for div in divs:
        title = div.find("a", {"class": "meta-title-link"})
        resume = div.find("div", {"class": "content-txt"})
        note = div.find("span", {"class": "stareval-note"})
        if note is None:
            note = "Aucune note"
            print(title.text, resume.text, note)
        else:    
            print(title.text, resume.text, note.text)
        # moyenne = 0
        # for note in notes:
        #     moyenne += float(note.text)
        # moyenne /= 2
        # print(moyenne)

    # Changement de page
    page += 1
    oldUrl = response.url
    response = requests.get(baseUrl + aucineUri + str(page))
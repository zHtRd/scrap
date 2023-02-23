# Imports
import requests
from bs4 import BeautifulSoup
import csv

# Variables
baseUrl = 'https://www.allocine.fr'
aucinemaUri = "/film/aucinema/?page="


# Création d'une nouvelle Swoup
def newSwoup(url, process):
    response = requests.get(url)
    if response.ok:
        swoup = BeautifulSoup(response.text, 'html.parser')
        return process(swoup)
    return []

# Get lien des affiches de fiche
def getMoviePage(swoup):
    links = []
    divs = swoup.findAll("div", {"class": "card entity-card entity-card-list cf"})
    for div in divs:
        a = div.find("a")
        links.append(baseUrl + a["href"])
    return links

def getMoviePages():
    pageNumber = 1
    oldUrl = ""
    response = requests.get(baseUrl + aucinemaUri + str(pageNumber))
    moviePageLinks = []

    while response.ok and response.url != oldUrl:
        moviePageLinks.extend(newSwoup(baseUrl + aucinemaUri + str(pageNumber),  getMoviePage)) 

        pageNumber += 1
        oldUrl = response.url
        response = requests.get(baseUrl + aucinemaUri + str(pageNumber))

    return moviePageLinks

def getInfos(swoup):
    title = swoup.find("div", {"class": "titlebar-title titlebar-title-lg"})
    
    return title

# Récupère infos des pages
def getPage(file):
    links = []
    links = fileReader(file)
    
    infos = []
    for link in links:
        infos.append(newSwoup(link.get("Page link"), getInfos))

    return infos


# Lecture d'un fichier
def fileReader(file):
    result = []
    with open(file, 'r', encoding="UTF8", newline="") as f:
        reader = csv.DictReader(f)
        for line in reader:
           result.append(line) 
    return result

# Ecriture sur un fichier
def fileWriter(file, fieldnames, data):
    with open(file, 'w', encoding="UTF8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        # writer.writerows(data)
        for el in data:
            f.write(el + '\n')
    return fileReader(file)


def main():
    links = getMoviePages()
    linkFields = ['Page link']
    fileWriter('links.csv', linkFields, links)

    getPage('links.csv')
    
    # movieFields = ['Titre', 'Résumé', 'Note']
    # fileWriter('infos.csv', movieFields, )

main()
exit()
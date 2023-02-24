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

# Récupère tous les liens de chaques pages
def getMoviePages():
    pageNumber = 1
    oldUrl = ""
    response = requests.get(baseUrl + aucinemaUri + str(pageNumber))
    moviePageLinks = []
    # moviePageLinks.extend(newSwoup(baseUrl + aucinemaUri + str(pageNumber),  getMoviePage)) 

    while response.ok and response.url != oldUrl:
        moviePageLinks.extend(newSwoup(baseUrl + aucinemaUri + str(pageNumber),  getMoviePage)) 

        pageNumber += 1
        oldUrl = response.url
        response = requests.get(baseUrl + aucinemaUri + str(pageNumber))

    return moviePageLinks


# Récupère infos des pages
def getInfosByPage(swoup):
    films = []
    
    fiche = swoup.find("main")
    if fiche is not None:
        title = tryToCleanOrReturnBlank(fiche.find("div", {"class": "titlebar-title titlebar-title-lg"}))
        note = tryToCleanOrReturnBlank(fiche.find("span", {"class": "stareval-note"}))
        
        details = tryToCleanOrReturnBlank(fiche.find("div", {"class": "meta-body-item meta-body-info"}))
        cleanDetail = []
        for ele in str(details).split("\n"):
                if ele != "":
                        cleanDetail.append(ele.lstrip("\n").lstrip(","))
                        details = " ".join(cleanDetail)
                        details = details.split('/')
        # duration = details[1].strip()
        categories = details[-1].strip()

        film = {
            'title': title,
            # 'duration': duration,
            'categories': categories,
            'note': note,
            # 'detail': detail,
            # 'categories': categories,  
        }
        films.append(film)
    return films

# Clean les valeurs 
def tryToCleanOrReturnBlank(str):
    try:
        result = str.getText().strip()
    except:
        result = ''
    return result

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
        writer.writerows(data)
    return fileReader(file)


def main():
    # Partie liens
    links = getMoviePages()

    rows = []
    for link in links:
        row = {}
        row['link'] = link
        rows.append(row)
    linkFields = ['link']
    fileWriter('links.csv', linkFields, rows)

    # Partie informations
    movies = []
    for link in fileReader('links.csv'):
        movies.extend(newSwoup(link['link'], getInfosByPage))
    # print(dict(sorted(movies.items(), key=lambda item: item[2])))

    movieFields = ['title', 'categories', 'note']
    fileWriter('movies.csv', movieFields, movies)

main()
exit()
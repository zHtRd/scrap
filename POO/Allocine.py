# Imports
from Toolkit import Toolkit
from AllocineEntry import AllocineEntry

# Classe Allocine (Site)
class Allocine:
    # Consturucteur
    def __init__(self, baseUrl, uri, nbPage):
        self.baseUrl = baseUrl
        self.uri = uri
        self.nbPage = nbPage
        self.urls = []
        self.links = []
        self.result = []
        self.finalFileNameFields = ["title", "categories", "note"]
    
    # Renvoie les Urls de chaque page 
    def getUrls(self):
        # for i in range(self.nbPage):
        i = 1
        while i <= self.nbPage: 
            self.urls.append(self.baseUrl + self.uri + str(i))
            i += 1
        return self.urls

    # Récupère les liens de chaque fiche de film
    def setLinks(self,swoup):
        divs = swoup.findAll("div", {"class": "card entity-card entity-card-list cf"})
        links = []
        for div in divs:
            a = div.find("a")
            try: 
                links.append(a['href'])
            except:
                pass
        self.links.extend(Toolkit.addBaseUrl(self.baseUrl, links))
        return self.links
    # Renvoie les liens de chaque fiche de film
    def getLinks(self):
        return self.links

    # Renvoie les fields du fichier finale
    def getFinalFieldNames(self):
        return self.finalFileNameFields
    
    # Récupère et renvoie les informations scrappées
    def getInfoByPage(self, swoup):
        films = []
    
        fiche = swoup.find("main")
        if fiche is not None:
            title = Toolkit.tryToCleanOrReturnBlank(fiche.find("div", {"class": "titlebar-title titlebar-title-lg"}))
            note = Toolkit.tryToCleanOrReturnBlank(fiche.find("span", {"class": "stareval-note"}))
            
            details = Toolkit.tryToCleanOrReturnBlank(fiche.find("div", {"class": "meta-body-item meta-body-info"}))
            cleanDetail = []
            for ele in str(details).split("\n"):
                    if ele != "":
                            cleanDetail.append(ele.lstrip("\n").lstrip(","))
                            details = " ".join(cleanDetail)
                            details = details.split('/')
            # duration = details[1].strip()
            categories = details[-1].strip()

            film = AllocineEntry(title, categories, note)
            films.append(film)
        self.result.extend(films)
        return films
    
    # Renvoie le résultat final du scrap
    def getResult(self):
        return self.result

    # Renvoie le result en dictionnaire
    def getDictResult(self):
        result = []
        for res in self.getResult():
            result.append(res.getDictEntry())
        return result
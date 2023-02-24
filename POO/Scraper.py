# Imports
import requests 
from bs4 import BeautifulSoup 
from Toolkit import Toolkit

# Classe scrapping
class Scraper:
    # Constructeur
    def __init__(self, ScrapInstance, linkFile, finalFile):
        self.setScrapInstance(ScrapInstance)
        self.setFinalFile(finalFile)
        self.setLinkFile(linkFile)
        self.finalFileNameFields = self.ScrapInstance.getFinalFieldNames()
        self.linkFileNameFields = ['link']

    # Instancie self scrap instance
    def setScrapInstance(self, instance):
        self.ScrapInstance = instance
        return self

    # Instancie le chemin du fichier des liens
    def setLinkFile(self, filePath):
        self.linkFile = filePath
        return self
    
    # Instancie le chemin du fichier final
    def setFinalFile(self, filePath):
        self.finalFile = filePath
        return self

    # Créer une nouvelle Swoup d'un Url
    def newSwoup(self, url, process):
        response = requests.get(url)
        if response.ok:
            swoup = BeautifulSoup(response.text, 'html.parser')
            try:
                return process(swoup)
            except Exception:
                print("ERROR: Impossible to process ! On :" + str(url))
                return False
        else:
            print("ERROR: Failed Connect on :" + str(url))
            return False
        return []

    # Créer une nouvelle Swoup pour chaque Urls
    def swoupMultiple(self, urls, process):
        result = []
        for url in urls:
            swoup = self.newSwoup(url, process)
            if hasattr(swoup, '__len__'):
                result.extend(swoup)
            else: 
                result.append(swoup)
        return result

    # Récupère les liens de films, chaques infos, puis les écrit 
    def exec(self):
        self.swoupMultiple(self.ScrapInstance.getUrls(), self.ScrapInstance.setLinks)

        rows= []
        for url in self.ScrapInstance.getLinks():
            row = {}
            row["link"] = url
            rows.append(row)
        Toolkit.fileWriter(self.linkFile, self.linkFileNameFields, rows)

        self.swoupMultiple(self.ScrapInstance.getLinks(), self.ScrapInstance.getInfoByPage)
        Toolkit.fileWriter(self.finalFile, self.finalFileNameFields, self.ScrapInstance.getDictResult())
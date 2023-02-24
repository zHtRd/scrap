# Imports
from Scraper import Scraper
from Allocine import Allocine

# Urls
baseUrl = 'https://www.allocine.fr'
aucinemaUri = "/film/aucinema/?page="

# Instanciation site Allocine
allocineInstance = Allocine(baseUrl, aucinemaUri, 14)

# Instanciation Scrapping d'Allocine
scraper = Scraper(allocineInstance, "POO/links.csv", "POO/movies.csv")
# Exécute le scrap
scraper.exec()
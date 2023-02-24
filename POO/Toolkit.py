# Import
import csv

# Classe Tools
class Toolkit:
    # Nettoie la variable
    def tryToCleanOrReturnBlank(str):
        try:
            result = str.getText().strip()
        except:
            result = ""
        return result

    # Ecrit dans un fichier les data au format csv
    def fileWriter(file,fieldnames, data):
        with open(file, 'w', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    # Lie la base Url à chaque Uri
    def addBaseUrl(baseUrl, urls):
        res = []
        for url in urls:
            res.append(baseUrl + url)
        return res
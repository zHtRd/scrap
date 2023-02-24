# Classe informations des pages films
class AllocineEntry:
    # Constructeur
    def __init__(self, title, categories, note):
        self.title = title
        self.categories = categories
        self.note = note
    
    # Renvoie les valeurs stockées
    def getDictEntry(self):
        return {
            "title": self.title,
            "categories": self.categories,
            "note": self.note
        }
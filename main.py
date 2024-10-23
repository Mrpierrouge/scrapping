from scrapping import scrap
from use_data import get_data, get_circular_diagram, get_bar_diagram, get_pdf
import matplotlib.pyplot as plt

def interface():
    while True:
        input_user = input('Que voulez-vous faire ?\n1 - scrapper les données (cela peux prendre quelques minutes)\n2 - Voir des données (les données doivent avoir été scrapper)\n3 - Créer un PDF  \n4 - Quitter')
        if input_user == "1":
            scrap()
            print("scrapping terminé")
        elif input_user == "2":
            new_input_user = input('Quelles données voulez-vous afficher ?\n1 - Diagramme circulaire\n2 - Diagramme en barres\n3 - Annuler\n')
            if new_input_user == "3":
                break
            else:
                try:
                    get_data()
                    if new_input_user == "1":
                        get_circular_diagram(True)
                    elif new_input_user == "2":
                        get_bar_diagram(True)
                except:
                    print("Vous devez d'abord scrapper les données")
        elif input_user == "3":
            try:
                get_data()
                get_pdf()
                print('pdf créé')
            except:
                print("Vous devez d'abord scrapper les données")
        elif input_user == "4":
            break
interface()
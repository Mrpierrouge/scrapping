import matplotlib.pyplot as plt
import csv
import os


all_datas = []          #using a global all_datas variable to call get_data fonction only once

def get_data():
    #récupère les données de tous les fichiers csv dans le dossier dossier_csv
    global all_datas
    all_datas = []          #resetting the global all_datas variable to avoid appending the same data multiple times
    for root, dirs, files in os.walk('dossier_csv'):
        for file in files:
            chemin_fichier = os.path.join(root, file)
            with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
                category_data = list(csv.DictReader(fichier, delimiter=';'))
                all_datas.append(category_data)       
    return None

def get_circular_diagram():
    #créer le diagramme criculaire de la répartition des livres dans chaque catégorie
    values = []
    labels = []
    for i in range (len(all_datas)):
        values.append(len(all_datas[i]))
        labels.append(all_datas[i][0]['product_category'])
    plt.figure(figsize=(18, 9))
    plt.pie(values)
    plt.legend(labels, loc='best', ncol=2)
    plt.axis('equal')  
    plt.show()
    return None

def get_category_medium_price(category): 
    #receive a category, a list of product, and return the average price those products
    prix = sum([float(product['product_including_tax'].replace('£', '')) for product in category]) / len(category)
    return prix

def get_bar_diagram(): 
    #créer le diagramme en barres des prix de livre moyens par catégorie
    values = []
    labels = []
    for i in range (len(all_datas)):
        prix = get_category_medium_price(all_datas[i])
        values.append(prix)
        labels.append(all_datas[i][0]['product_category'])
    plt.bar(labels, values)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
    return None
    
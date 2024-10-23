import matplotlib.pyplot as plt
import csv
import os


all_datas = []          #using a global all_datas variable to call get_data fonction only once

def get_data():
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
    values = []
    labels = []
    for i in range (len(all_datas)):
        values.append(len(all_datas[i]))
        labels.append(all_datas[i][0]['product_category'])
    plt.pie(values, labels=labels)
    plt.show()
    return None

def get_category_medium_price(category):

    prix = sum([float(product['product_including_tax'].replace('£', '')) for product in category]) / len(category)
    return prix

def get_bar_diagram():
    values = []
    labels = []
    for i in range (len(all_datas)):
        prix = get_category_medium_price(all_datas[i])
        values.append(prix)
        labels.append(all_datas[i][0]['product_category'])
    plt.bar(labels, values)
    plt.show()
    return None
    
get_data()
# get_circular_diagram()
get_bar_diagram()
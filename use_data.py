import matplotlib.pyplot as plt
import csv
import os
from scrapping import folder_maker
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

all_datas = []          #using global variables to call get_data fonction only once
all_prices = []
category_counts = {}

def get_data():
    #récupère les données de tous les fichiers csv dans le dossier dossier_csv
    global all_datas
    global all_prices
    global category_counts
    all_datas = []          #resetting the global variables to avoid appending the same data multiple times        
    all_prices = []
    category_counts = {}
    for root, dirs, files in os.walk('dossier_csv'):
        for file in files:
            chemin_fichier = os.path.join(root, file)
            with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
                category_data = list(csv.DictReader(fichier, delimiter=';'))
                all_datas.append(category_data)       
                category_price = get_category_medium_price(category_data)
                all_prices.append(category_price)
                category_name = category_data[0]['product_category']
                category_counts[category_name] = len(category_data)
    return None

def get_circular_diagram(is_from_main):
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
    plt.savefig('dossier_graphique/diagramme_circulaire.png')
    if is_from_main:
        plt.show()
    else:
        plt.close()
    return None

def get_category_medium_price(category): 
    #receive a category, a list of product, and return the average price those products
    try:
        prix = sum([float(product['product_including_tax'].replace('£', '')) for product in category]) / len(category)
        return prix
    except ZeroDivisionError:
        print('La catégorie est vide')
        return None

def get_bar_diagram(is_from_main): 
    #créer le diagramme en barres des prix de livre moyens par catégorie
    values = []
    labels = []
    for i in range (len(all_datas)):
        prix = get_category_medium_price(all_datas[i])
        values.append(prix)
        labels.append(all_datas[i][0]['product_category'])
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('dossier_graphique/diagramme_barres.png')
    if is_from_main:
        plt.show()
    else:
        plt.close()
    return None

def get_pdf():
    #créer un pdf avec les diagrammes circulaires et en barres
    folder_maker('dossier_graphique')
    get_circular_diagram(False)
    get_bar_diagram(False)
    pdf_file = 'rapport_prix_livres.pdf'
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, "Rapport des prix des livres par catégorie")

    try :
        medium_prices = sum(all_prices) / len(all_prices)
    except ZeroDivisionError:
        print("Aucune catégorie n'a été scrapper")
    most_represented_category = max(category_counts, key=category_counts.get)
     
    c.setFont("Helvetica", 12)
    
    c.drawString(100, height - 100, f"Prix moyen global des livres : £{medium_prices}")
    c.drawString(100, height - 125, f"Catégorie la plus représentée : {most_represented_category} ({category_counts[most_represented_category]} livres)")
    c.drawString(100, height - 170, "Diagramme circulaire de la répartition des livres par catégorie :")
    pie_chart = ImageReader('dossier_graphique/diagramme_circulaire.png')
    c.drawImage(pie_chart, 100, height - 425, width=500, height=250)  
    c.drawString(100, height - 450, "Diagramme en barres des prix moyens des livres par catégorie")
    bar_chart = ImageReader('dossier_graphique/diagramme_barres.png')
    c.drawImage(bar_chart, 100, height - 725, width=500, height=250)  

    c.showPage()
    c.save()    
    return None

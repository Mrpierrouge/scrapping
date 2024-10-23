import matplotlib.pyplot as plt
import csv
import os
from scrapping import folder_maker
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

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
    plt.savefig('dossier_graphique/diagramme_circulaire.png')
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
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('dossier_graphique/diagramme_barres.png')
    return None

def get_pdf():
    #créer un pdf avec les diagrammes circulaires et en barres
    folder_maker('dossier_graphique')
    get_circular_diagram()
    plt.close()
    get_bar_diagram()
    plt.close()
    pdf_file = 'rapport_prix_livres.pdf'
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, "Rapport des prix des livres par catégorie")

    c.drawString(100, height - 100, "Diagramme circulaire de la répartition des livres par catégorie")
    pie_chart = ImageReader('dossier_graphique/diagramme_circulaire.png')
    c.drawImage(pie_chart, 100, height - 400, width=400, height=300)  
    c.drawString(100, height - 450, "Diagramme en barres des prix moyens des livres par catégorie")
    bar_chart = ImageReader('dossier_graphique/diagramme_barres.png')
    c.drawImage(bar_chart, 100, height - 750, width=400, height=300)  

    c.showPage()
    c.save()
    return None
import requests
from bs4 import BeautifulSoup
import csv
import os
import shutil

site_url = 'https://books.toscrape.com/'
category_url = '' #need this variable global to be able to use it in the recursive function category_explorer

def get_soup(url):
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Authorization': 'Bearer YOUR_API_TOKEN'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Requête réussie!")
    else:
        print(f"Erreur : {response.status_code}")
    return BeautifulSoup(response.content, 'html.parser')


def get_int_from_string(string):
    number = ''
    for l in string:
        if l.isdigit():
            number += l
    if number == '':
        number = 0
    else:
        number = int(number)
    return number


def category_explorer(url, category_products): #recursive function, receive a category url and the current datas of the category, calls page_explorer for each page of the category
    category_page = get_soup(url)
    page_explorer(category_page, category_products)
    if category_page.find('li', class_='next'):
        next_page_url = category_page.find('li', class_='next').find('a')['href']
        print('on passe à la page suivante', category_url + next_page_url)
        category_explorer(category_url + next_page_url, category_products)
    else:
        print('fini')
    return category_products

def page_explorer(page, category_products): # receive a page and the current datas of the category, extract the datas of the page and add them to the category datas
    for product in page.find_all('h3'):
        product_url = product.find('a')['href'].replace('../', '')
        product_page = get_soup('https://books.toscrape.com/catalogue/' + product_url)

        product_table = product_page.find('table')
        universal_product_code = product_table.find_all('td')[0].text
        product_title = product_page.find('h1').text

        product_including_tax = product_table.find_all('td')[3].text
        product_excluding_tax = product_table.find_all('td')[2].text

        product_number_available = get_int_from_string(product_table.find_all('td')[5].text)

        product_description = product_page.find_all('p')[3].text
        product_category = product_page.find_all('a')[3].text
        product_review_rating = product_page.find('p', class_='star-rating')['class'][1]
        
        product_image_url = product_page.find('img')['src']
        product_image_url = product_image_url.replace('../', '')
        product_image_url = 'https://books.toscrape.com/' + product_image_url
        category_products.append({
            'universal_product_code': universal_product_code,
            'product_title': product_title,
            'product_including_tax': product_including_tax,
            'product_excluding_tax': product_excluding_tax,
            'product_number_available': product_number_available,
            'product_description': product_description,
            'product_category': product_category,
            'product_review_rating': product_review_rating,
            'product_image_url': product_image_url
        })
    return None

caracteres_interdits = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

def clean_name(nom):
    # Remplacer les caractères interdits par des underscores
    for char in caracteres_interdits:
        nom = nom.replace(char, '_')
    return nom


def download_image(url_image, nom_image, category): #receive an image url, a name and a category, download the image and save it in the folder_images of this category
    response = requests.get(url_image)
    nom_image = clean_name(nom_image)
    nom_dossier = clean_name(category)
    chemin_image = os.path.join('dossier_images', nom_dossier, nom_image + '.jpg')    
    with open(chemin_image, 'wb') as fichier:
        fichier.write(response.content)
    print(f"Image {nom_image} téléchargée avec succès!")
    return None

def file_writer(category_name, products):  # receive a category name and the datas of this category, create the files (jpg and csv) for this category
    folder_maker('dossier_csv/' + category_name)
    folder_maker('dossier_images/' + category_name)
    chemin_csv = os.path.join('dossier_csv', category_name, category_name + '.csv')
    with open(chemin_csv, 'w', newline='', encoding='utf-8-sig') as fichier_csv:
        writter = csv.writer(fichier_csv, delimiter=';')
        writter.writerow(['universal_product_code', 'product_title', 'product_including_tax', 'product_excluding_tax', 'product_number_available', 'product_description', 'product_category', 'product_review_rating', 'product_image_url'])
        for product in products:
            download_image(product['product_image_url'], product['product_title'], product['product_category'])
            writter.writerow([product['universal_product_code'], product['product_title'], product['product_including_tax'], product['product_excluding_tax'], product['product_number_available'], product['product_description'], product['product_category'], product['product_review_rating'], product['product_image_url']])
    return None

def site_explorer(): # main function, calls category_explorer for each category found and call file_writer to write the files
    global category_url
    site = get_soup(site_url)
    for category in site.find('ul', class_='nav nav-list').find('ul').find_all('a'):
        category_name = category.text.strip()
        category_url = site_url + category['href'].replace('index.html', '')         # need to remove index.html for category_explorer to work properly, as it adds page-x.html at the end of the url. calling a path without index.html still opens it
        category_products = category_explorer(category_url, [])
        file_writer(category_name, category_products)
    return None   

def folder_maker(path): #delete the folder if it exists and create it as an empty folder
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def scrap():
    folder_maker('dossier_images')
    folder_maker('dossier_csv')
    site_explorer()
    return None
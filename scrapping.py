import requests
from bs4 import BeautifulSoup
import csv
import os

site_url = 'https://books.toscrape.com/'

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


def category_explorer(url):
    category_page = get_soup(url)
    page_explorer(category_page)
    if category_page.find('li', class_='next'):
        next_page_url = category_page.find('li', class_='next').find('a')['href']
        print('on passe à la page suivante', next_page_url)
        category_explorer(category_url + next_page_url)
    else:
        print('fini')
    return None

def page_explorer(page):
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
        all_products.append({
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


def download_image(url_image, nom_image):
    response = requests.get(url_image)
    nom_image = clean_name(nom_image)
    chemin_image = os.path.join('dossier_images', nom_image + '.jpg')
    
    print(chemin_image)
    with open(chemin_image, 'wb') as fichier:
        fichier.write(response.content)
    print(f"Image {nom_image} téléchargée avec succès!")
    
site = get_soup(site_url)
category_url = 'https://books.toscrape.com/catalogue/category/books/sequential-art_5/'

all_products= []

category_explorer(category_url)

if not os.path.exists('dossier_images'):
    os.makedirs('dossier_images')
    
with open('products.csv', 'w', newline='', encoding='utf-8-sig') as fichier_csv:
    writter = csv.writer(fichier_csv, delimiter=';')
    writter.writerow(['universal_product_code', 'product_title', 'product_including_tax', 'product_excluding_tax', 'product_number_available', 'product_description', 'product_category', 'product_review_rating', 'product_image_url'])
    for product in all_products:
        print(product['product_image_url'])
        download_image(product['product_image_url'], product['product_title'])
        writter.writerow([product['universal_product_code'], product['product_title'], product['product_including_tax'], product['product_excluding_tax'], product['product_number_available'], product['product_description'], product['product_category'], product['product_review_rating'], product['product_image_url']])
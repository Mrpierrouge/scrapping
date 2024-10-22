import requests
from bs4 import BeautifulSoup
import csv

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
    return BeautifulSoup(response.text, 'html.parser')


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

site = get_soup(site_url)


all_products= []


product_page = get_soup('https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html')

universal_product_code = product_page.find('table').find_all('td')[0].text
product_title = product_page.find('h1').text

product_including_tax = product_page.find('table').find_all('td')[3].text
product_excluding_tax = product_page.find('table').find_all('td')[2].text

product_number_available_string = product_page.find('table').find_all('td')[5].text
product_number_available = get_int_from_string(product_number_available_string)

product_description = product_page.find_all('p')[3].text
product_category = product_page.find_all('a')[3].text
product_review_rating = product_page.find('p', class_='star-rating')['class'][1]
product_image_url = product_page.find('img')['src']

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

"""
Step 4 télécharger et enregistrer les fichiers images de chaque page Produit
"""

import requests
import csv
import time
from bs4 import BeautifulSoup
import os

# Créer un dossier pour stocker les images
if not os.path.exists('images'):
    os.makedirs('images')

# URL de base
base_url = 'http://books.toscrape.com/catalogue/'

# Fonction pour extraire les informations de chaque page de produit
def scrape_product_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('h1').text
    img_url = soup.find('div', class_='item active').img['src']
    img_url = img_url.replace('../', '')
    return title, img_url

# Récupérer les liens des pages de produit de toutes les pages
page_number = 1
product_links = []
while True:
    response = requests.get(f"{base_url}page-{page_number}.html")
    if response.status_code == 404:
        break
    soup = BeautifulSoup(response.content, 'html.parser')
    product_links += [base_url + a['href'] for a in soup.select('h3 > a')]
    page_number += 1

# Télécharger les images de chaque page de produit
for link in product_links:
    try:
        title, img_url = scrape_product_page(link)
        img_path = os.path.join('images', f'{title}.jpg')
        response = requests.get(base_url + img_url)
        with open(img_path, 'wb') as f:
            f.write(response.content)
            print(f'Saved image: {img_path}')
    except Exception as e:
        print(f"Error downloading image from {link}: {e}")
    time.sleep(2) # pause de 2 secondes entre chaque requête

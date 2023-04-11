""""
Step 2  Scrape de l'URL de la page Produit de chaque livre appartenant à cette catégorie.
"""

import requests
from bs4 import BeautifulSoup
import csv
import time

def get_product_links(url):
    response = requests.get(url)
    if response.status_code == 200:
        print("Request Successful")
        soup = BeautifulSoup(response.text, "html.parser")
        product_links = soup.find_all("h3")
        product_urls = []
        for link in product_links:
            product_url = link.find("a")["href"].replace("../../../", "http://books.toscrape.com/catalogue/")
            product_urls.append(product_url)
        
        next_link = soup.find("li", {"class": "next"})
        if next_link:
            next_url = next_link.find("a")["href"]
            next_url = url.rsplit('/', 1)[0] + '/' + next_url
            next_product_urls = get_product_links(next_url)
            product_urls += next_product_urls
        return product_urls
    else:
        print("La requête GET a échoué avec le code d'erreur: ", response.status_code)
        return []

def write_product_links_to_csv(product_urls, filename):
    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Product Page URL"])
        for url in product_urls:
            writer.writerow([url])

def step2():
    # URL de la catégorie choisie
    category_url = "http://books.toscrape.com/catalogue/category/books/childrens_11/index.html"

    # Obtenir les URLs des pages produits dans la catégorie
    product_urls = get_product_links(category_url)

    # Écrire les URLs des pages produits dans un fichier CSV
    write_product_links_to_csv(product_urls, "book_data.csv")

    # Attendre un peu pour éviter de surcharger le site web
    time.sleep(1)

    # Récupérer les informations de chaque livre et les stocker dans le CSV
    # à compléter selon les besoins

    print("Les URLs des pages produits ont été extraites avec succès.")

step2()



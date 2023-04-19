"""
Step 1 : scraper des informations sur un livre
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import os

def scrape_book_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        print("Request successful")
    else:
        print("Request failed")
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    
    book_data = [
        url,
        get_upc(soup),
        get_title(soup),
        get_price_incl_tax(soup),
        get_price_excl_tax(soup),
        get_availability(soup),
        get_description(soup),
        get_category(soup),
        get_review_rating(soup),
        get_image_url(soup)
    ]

    return book_data

def get_upc(soup):
    upc = soup.select_one("table tr:nth-of-type(1) td").text
    return upc

def get_title(soup):
    title = soup.select_one(".product_main h1").text
    return title

def get_price_incl_tax(soup):
    price_incl_tax = soup.select_one("table tr:nth-of-type(4) td").text
    return price_incl_tax

def get_price_excl_tax(soup):
    price_excl_tax = soup.select_one("table tr:nth-of-type(3) td").text
    return price_excl_tax

def get_availability(soup):
    availability = soup.select_one("table tr:nth-of-type(6) td").text
    return availability

def get_description(soup):
    description = soup.select_one("#product_description + p").text
    return description

def get_category(soup):
    category = soup.select_one(".breadcrumb li:nth-of-type(3) a").text
    return category

def get_review_rating(soup):
    rating_classes = ["One", "Two", "Three", "Four", "Five"]
    for rating_class in rating_classes:
        if soup.select_one(".product_page .star-rating." + rating_class) is not None:
            return rating_class
    return None

def get_image_url(soup):
    image_url = soup.select_one(".carousel-inner img")["src"]
    return image_url

def save_to_csv(book_data):
    
    fieldnames = [
        "Product page url",
        "Universal product code (upc)",
        "Title",
        "Price including tax",
        "Price excluding tax",
        "Number available",
        "Product description",
        "Category",
        "Review rating",
        "Image url\n"
    ]

    with open("book_data.csv", "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for book in book_data:
            writer.writerow(dict(zip(fieldnames, book)))

def step1():
    book_data = scrape_book_data("http://books.toscrape.com/catalogue/birdsong-a-story-in-pictures_975/index.html")
    save_to_csv([book_data])
    print

step1()

""""
Step 2  Scrape de l'URL de la page Produit de chaque livre appartenant à cette catégorie.
"""

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

"""
Step 3 extraction de toutes les catégories de livres disponibles
"""

# Créer un dossier pour stocker les fichiers CSV
if not os.path.exists("data/"):
    os.makedirs("data/")

BASE_URL = "http://books.toscrape.com/"

def extract_categories():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, "html.parser")
    categories = soup.find("div", {"class": "side_categories"}).find_all("a")
    return [BASE_URL + category["href"] for category in categories]

def extract_book_data(category_url):
    page_url = category_url
    book_data = []
    while True:
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, "html.parser")
        books = soup.find_all("article", {"class": "product_pod"})
        for book in books:
            title = book.h3.a["title"]
            url = BASE_URL + book.h3.a["href"]
            price_incl = book.find("p", {"class": "price_color"}).get_text()
            price_excl = book.find("p", {"class": "price_color"}).get_text()
            availability = book.find("p", {"class": "availability"}).get_text().strip()
            rating = ' '.join(book.find('p', {'class': 'star-rating'})['class']).replace('star-rating', '').strip()
            image_url = BASE_URL + book.find('img')["src"].replace("../", "")
            product_description = soup.find('div', {"id": "product_description"})
            description = product_description.find_next("p").get_text() if product_description else ""
            book_data.append([title, url, price_incl, price_excl, availability, description, category_url.split("/")[-2], rating, image_url])
            
        next_button = soup.find("li", {"class": "next"})
        if next_button:
            page_url = category_url.replace("index.html", "") + next_button.a["href"]
        else:
            break
    return book_data


def write_to_csv(category_name, book_data):
    with open(f"data/{category_name}.csv", "a", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Title", "URL", "Price (excl. tax)", "Price (incl. tax)", "Availability", "Description", "Category","Rating","Image URL"])
        writer.writerows(book_data)

def scrape_books_from_category(category_url):
    book_data = extract_book_data(category_url)
    category_name = category_url.split("/")[-2]
    write_to_csv(category_name, book_data)
    print(f"Les informations ont été extraites pour la catégorie {category_name}.")
    time.sleep(0.5)

def step3():
    category_urls = extract_categories()
    for category_url in category_urls:
        scrape_books_from_category(category_url)

if __name__ == "__main__":
    step3()

"""
Step 4 télécharger et enregistrer les fichiers images de chaque page Produit
"""

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


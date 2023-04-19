"""
Step 3 extraction de toutes les catégories de livres disponibles
"""
# Importer les modules nécessaires
import requests
import csv
import time
from bs4 import BeautifulSoup
import os

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
            description = product_description.find_next("p").get_text() if product_description else ''
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

#Phase 3 extraction de toutes les catégories de livres disponibles

import requests
from bs4 import BeautifulSoup

fieldsName = [
    "Product page url",
    "Universal product code (upc)",
    "Title",
    "Price including tax",
    "Price excluding tax",
    "Number available",
    "Product description",
    "Category",
    "Review rating",
    "Image url"
]

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
    return soup.select_one("table tr:nth-of-type(1) td").text

def get_title(soup):
    return soup.select_one(".product_main h1").text

def get_price_incl_tax(soup):
    return soup.select_one("table tr:nth-of-type(4) td").text

def get_price_excl_tax(soup):
    return soup.select_one("table tr:nth-of-type(3) td").text

def get_availability(soup):
    return soup.select_one("table tr:nth-of-type(6) td").text

def description(soup):
    return soup.select_one("#product_description + p").text

def get_category(soup):
    return soup.select_one(".breadcrumb li:nth-of-type(3) a").text

def get_review_rating(soup):
    return soup.select_one(".product_page .star-rating")["class"][1]
    
def get_image_url(soup):
    return soup.select_one(".carousel-inner img")["src"]

# Fonction pour suavegarder les information produit dans un fichier csv
def save_to_csv(book_data):

    with open("book_data.csv", "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldsName)
        writer.writerow(book_data)

# book_data = scrape_book_data('http://books.toscrape.com/catalogue/birdsong-a-story-in-pictures_975/index.html')
# save_to_csv(book_data)
# print(book_data)

# STEP 2

def get_product_urls(url):
    """
    Cette fonction prend en compte une URL et renvoie une liste de toutes les URL de produits sur cette page.
    """
    # Faire une requette de l'url
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Trouver toutes les URL des produits sur la page
    product_urls = []
    for product in soup.find_all('article', class_='product_pod'):
        product_url = product.find('a')['href']
        product_urls.append('http://books.toscrape.com/catalogue/' + product_url)

    return product_urls

# url = 'http://books.toscrape.com/catalogue/category/books/childrens_11/index.html'
# product_urls = get_product_urls(url)
# print(product_urls)

# with open("book_data.csv", "w", newline="", encoding="utf-8") as csv_file:
#     writer = csv.DictWriter(csv_file, fieldnames=fieldsName)
#     writer.writeheader()

# for url in product_urls:
#     book_data = scrape_book_data(url)
#     save_to_csv(book_data)

# STEP 3

# function to retrieve book category URLs
def get_category_urls():
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    categories = soup.select("ul.nav.nav-list > li > ul > li > a")
    category_urls = [url + c.get('href').replace("../", "") for c in categories]
    return category_urls


# retrieve all category URLs
category_urls = get_category_urls()

# retrieve product information for all books in all categories
for category_url in category_urls:
    product_urls = get_product_urls(category_url)
    print(product_urls)

    with open("book_data.csv", "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldsName)
        writer.writeheader()

    for url in product_urls:
        book_data = scrape_book_data(url)
        save_to_csv(book_data)
        # save_image(url) # A FAIRE pour le STEP 4!

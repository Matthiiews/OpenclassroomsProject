"""
Step 1 : scraper des informations sur un livre
"""

import requests
from bs4 import BeautifulSoup
import csv


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
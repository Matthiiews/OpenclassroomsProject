#Phase 4 télécharger et enregistrer les fichiers images de chaque page Produit
import requests
from bs4 import BeautifulSoup
import os

def download_images(url):
   
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extraire l'URL de l'image et le nom du fichier
    img_url = "http://books.toscrape.com/" + soup.find("div", class_="item active").img["src"][6:]
    img_name = soup.find("div", class_="item active").img["alt"]
    
    # Recuperer l'URL de l'image et l'enregistrer dans un fichier
    response = requests.get(img_url)
    if not os.path.exists('images'):
        os.makedirs("images")
    with open(f"images/{img_name}.jpg", "wb") as f:
        f.write(response.content)
    print(f"Downloaded {img_name} image.")

#Requette de la page web et extraire les URL de toutes les pages de produits.
if __name__ == "__main__":
    url = "http://books.toscrape.com/catalogue/category/books_1/index.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    book_urls = [a["href"] for a in soup.select("h3 > a")]
    
    # Télécharge les images de chaque page de produit
    for book_url in book_urls:
        download_images("http://books.toscrape.com/catalogue/" + book_url)

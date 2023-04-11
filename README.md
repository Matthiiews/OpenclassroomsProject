# OpenClassrooms Développeur d’application Python Project #2 : Utiliser les bases de Python pour l'analyse de marché 
# OpenClassrooms: Projet 2: Books To Scrape
Testé sur Windows 10, Python 3.11.2. 

# Objectifs 

Scraping de books.toscrape.com avec BeautifulSoup4 et Requests , exportez les données vers des fichiers .csv et téléchargez les images de couverture dans le dossier "exports" . 

Mise en place du processus ETL : 

.Extraire des données pertinentes et spécifiques du site Web source ; 

.Transformer, filtrer et nettoyer les données ; 

.Load (Chargez) les données dans des fichiers interrogeables et récupérables. 

Ce script permet de récupérer les informations de tout les produits sur le site http://books.toscrape.com/.
Ces informations sont les suivantes:
 - URL du livre
 - Universal Product Code (upc)
 - Titre du livre
 - Prix, taxe incluse
 - Prix, taxe exclue
 - Quantité disponible
 - Description du produit
 - Catégorie
 - Rating
 - URL de l'image
 - Chemin local de l'image téléchargée

Cas d'usage:

A. Récupère une page (un ouvrage) du site http://books.toscrape.com/ vers un fichier CSV.

B. Récupère tous les ouvrages d'une catégorie du site http://books.toscrape.com/ vers un fichier CSV.

C. Récupère toutes les catégories et tous les ouvrages du site http://books.toscrape.com/ vers des fichiers CSV organisés en catégories.

# Installation:

Commencez tout d'abord par installer Python.
Lancez ensuite la console, placez vous dans le dossier de votre choix puis clonez ce repository:
```
git clone https://github.com/Matthiiews/OpenclassroomsProject.git
```
Placez vous dans le dossier OpenclassroomsProject, puis créez un nouvel environnement virtuel:
```
python -m venv env
```
Ensuite, activez l'environnement virtuel.
Windows:
```
env\scripts\activate.bat
```
Linux:
```
source env/bin/activate
```
Il ne reste plus qu'à installer les packages requis:
```
pip install -r requirements.txt
```
Vous pouvez enfin lancer le script:
```
python main.py
```

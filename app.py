from flask import Flask, render_template, request
import re
import bleach
from pymongo.mongo_client import MongoClient
import pymongo
from dotenv import load_dotenv
import os

# Charger les variables du fichier .env
load_dotenv()

# création de l'application
app = Flask(__name__)


# Connexion a la db
mongo_url = os.getenv("MONGO_URL")
myclient = pymongo.MongoClient(mongo_url)
mydb = myclient['Arkis']
mycol = mydb["Flask"]

# créé une route pour accéder à mon serveur temp et accéder à la page "Home"
@app.route('/') 
def home():
    return render_template('index.html')
    
# Créé la route de la page de validation
@app.route('/retour', methods=['POST']) 

# Création de la fonction principale 
# Définition de la fonction de validation des données du formulaire, vérifaction des données, protection des données ainsi que renvoie vers la page de feedback.
def form_valide():
    
    # Fonction auxiliaire pour valider l'adresse email
    def email_valide(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email)
    
    # attribution des fonctions
    # empecher les scripts
    nom = bleach.clean(request.form.get('nom'))
    prenom = bleach.clean(request.form.get('prenom'))
    email = bleach.clean(request.form.get('email'))
    pays = bleach.clean(request.form.get('pays'))
    genre = bleach.clean(request.form.get('genre'))
    message = bleach.clean(request.form.get('message'))
    sujets = request.form.getlist('sujets')  # Utilisez getlist() pour récupérer une liste de valeurs
    honeypot = request.form.get('honeypot')  # Champ honeypot
      
    # Vérification des caractères dans "nom" et "prenom"
    if not re.match(r'^[A-Za-zÀ-ÿ\s-]+$', nom) or not re.match(r'^[A-Za-zÀ-ÿ\s-]+$', prenom):
        return "Le nom et le prénom doivent contenir uniquement des lettres et/ou être rempli."

    # Vérification de l'adresse email
    if not email_valide(email):
        return "Veuillez indiquer une adresse mail valide"

    # Vérification des champs obligatoires (nom, prenom, email, pays, genre, message)
    if not nom or not prenom or not email or not pays or not genre or not message:
        return "Veuillez remplir tous les champs du formulaire."
    
    # Faire en sorte que si aucun sujet n'est sélectionné alors le choix par défaut est "Autre"
    if not sujets:
        sujets = ["Autre"]
    
    # Vérification honeypot antispam
    if honeypot:
        return "Êtes-vous un robot ?"
    
    # insertion des données dans mongodb
    mycol.insert_one({
    "Nom": nom,
    "prenom": prenom,
    "email": email,
    "pays": pays,
    "genre": genre,
    "message": message,
    "sujets": sujets
    }) 
    # renvoyé toutes les infos entré sur la page retour.html pour avoir un feedback.
    return render_template('retour.html', prenom = prenom, nom = nom, email = email, pays = pays, genre = genre, message = message, sujets = sujets )


# Lancement de l'app via le terminal
if __name__ == "__main__":
    app.run(debug=True)

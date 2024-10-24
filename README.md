# This is a study project to scrap and use the data of a website in python 

# **Table des Matières**
- [Description](#description-)
- [Installation](#installation-)
- [Utilisation](#utilisation)
- [Structure du projet](#structure-de-projet-)
# **Description :**
Ce projet a été réaliser dans le cadre de mes études. Il s'agit d'un exercice de scrapping de données d'un site répertoriant des livre [(voir le site)](https://books.toscrape.com/).
<br>
On créer des fichiers de ses données pour en stockers les informations et les utiliser a d'autres fins (graphiques, pdf, etc)
<br>

# **Installation :**
- Clonez ce dépôt sur votre machine locale :

```bash 
git clone https://github.com/Mrpierrouge/scrapping.git
```

- installer les dépendances nécéssaires :

```bash 
pip install -r requirements.txt
```
<br>

# **Utilisation :**
- Exécutez le script principal main.py :
```bash
python main.py
```

# Structure de projet :
- ### ```requirement.txt``` :
    - nécéssaire pour installer les dépendances
- ### ```README.md``` :
    - ce fichier
- ### ```main.py``` :
     - fichier principal a éxécuter, appelant ```scrapping.py``` et ```use_data.py```
- ### ```scrapping.py``` :
    - fichier faisant le scrapping des données
- ### ```use_data.py``` :
    - - fichier utilisant les données 
- ### ```rapport_prix_livres.pdf``` :
    - fichier pdf créer par le script 
- ### dossier_csv :
    - dossier créer par le script et stockant un fichiers csv pour chaque catégorie de livres
- ### dossier_images : 
    - dossier créer par le script et stockant les images de tout les livres par catégorie
- ### dossier_graphique :
    - dossier créer par le script et stockant les images des graphiques





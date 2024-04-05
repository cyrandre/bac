# Maquette pour le projet bac++

Private version for Bac++

Cette maquette est un prototype de site web de questionnaire à choix multiple.
L'administrateur peut céer et éditer les questions qui seront proposées aux utilisateurs.
Lors d'une session, un nombre fixe de questions est tiré aléatoirement dans la base et envoyé
au client. L'ordre des propositions de réponse est également tiré aléatoirement. En mode _training_,
les réponses sont transmises avec les questions afin de présenter la solution après chaque question
avant de passer à la question suivante. En mode _test_, les réponses de l'utilisteur sont enregistrées
et retournées aux serveur en fin de questionnaire. Le serveur effectue alors la correction et renvoie le score.

## Installation

- Création d'un evironnement virtuel

```
python3 -m venv .venv
source .venv/bin/activate
```

- Installation des dépendances

```
pip install -r requirements.txt
```

## Démarrage

- Configuration des mails d'authentification
  
```
export MAIL_USERNAME = "user@mail.com"
export EMAIL_PASSWORD = "password"
```  

- Initialisation de la base de données

```
flask --app bac db init
flask --app bac db migrate
flask --app bac db upgrade
```

- Création d'un compte administrateur

```
flask --app create-admin
```

- Démarrage du serveur en mode debug

```
flask --app bac run --debug
```

## Utilisation

Le site est visible à l'adresse: http://127.0.0.1:5000
Lors de la première utilisation, la base de données est vide. Il n'y a donc aucune question ni utilisateur
enregistré.

### Enregistrement de l'administrateur

La connexion ou l'enregistrement d'un utilisateur se fait en cliquant sur l'icône en haut à droite de la page d'acceuil.

![alt text](https://github.com/cyrandre/bac--/blob/main/screenshots/user.png)

Pour créer des questions, il faut s'enregistrer en tant qu'administateur. Pour cela, il faut (pour l'instant) s'enregistrer en tant qu'_admin_
avec le mot de passe de son choix. Attention, un seul administateur est autorisé. Une fois celui-ci enregistré, il n'est pas possible de changer
le mot de passe. La seule façon de réinitialiser le mot de passe administrateur est d'effacer la base de donnée!

### Ajout et edition des questions

Le bouton _questions_, visible uniquement lorsque l'utilisateur est connecté en tant qu'admin, permet de visualiser toutes les questions enregistrées.
Un mini bouton permet de supprimer et éditer chacune d'elle. Le bouton _question_ dans la banière permet d'ajouter une nouvelle question.
La page d'ajout et d'édition des questions permets de modifier les éléments suivants:

- Titre de la question
- Détails de la question
- Images qui accompagne la question
- Légende des images (pas utilisé pour l'instant)
- Les choix de réponse proposés (hors solution)
- La ou les solutions attendues

Pour enregistrer une question, il faut a _minima_ que le titre et une solution soient fournis.
Les images sont ajoutées par _drag and drop_.

## Screenshots

**Page d'accueil**
![alt text](https://github.com/cyrandre/bac/blob/main/screenshots/home.png)
**Question**
![alt text](https://github.com/cyrandre/bac/blob/main/screenshots/question.png)
**Visualisation de toutes les questions**
![alt text](https://github.com/cyrandre/bac/blob/main/screenshots/vue_questions.png)
**Edition d'une question**
![alt text](https://github.com/cyrandre/bac/blob/main/screenshots/edition_question.png)

# 🩺 Skin Cancer — Application Web de Diagnostic

Application web développée avec **Flask** et **Deep Learning (VGG16)** permettant aux professionnels de santé de diagnostiquer des lésions cutanées (Bénigne ou Maligne) à partir d'images.

---

## 📋 Fonctionnalités

- 🔐 Authentification (Login)
- 🔬 Analyse d'image par le modèle VGG16
- 📊 Résultat avec taux de confiance
- 📋 Historique des patients
- 🗑️ Suppression d'un patient
- 💾 Stockage des données dans MySQL

---

## 🛠️ Technologies utilisées

| Catégorie | Technologie | Rôle |
|-----------|-------------|------|
| **Langage** | Python 3.x | Langage principal |
| **Framework web** | Flask | Serveur web & routing |
| **Templates** | Jinja2 | Moteur de rendu HTML |
| **Frontend** | Bootstrap 5 (CDN) | Mise en page & composants UI |
| **Frontend** | CSS personnalisé | Styles custom (`style.css`) |
| **Deep Learning** | TensorFlow / Keras | Chargement & inférence du modèle |
| **Modèle IA** | VGG16 (pré-entraîné) | Classification d'images cutanées |
| **Traitement image** | NumPy | Prétraitement des images |
| **Base de données** | MySQL | Stockage users & historique patients |
| **Connecteur DB** | mysql-connector-python | Interface Python ↔ MySQL |
| **Serveur local** | XAMPP | Hébergement MySQL en local |
| **Authentification** | Sessions Flask | Gestion des connexions utilisateur |
| **Upload fichiers** | Flask (multipart) | Réception des images soumises |

---

## 📁 Structure du projet

```
SKIN_CANCER_APP/
├── static/
│   ├── uploads/
│   └── style.css
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── predict.html
│   ├── result.html
│   └── patients.html
├── app.py
├── .gitignore
└── README.md
```
---

## 🔑 Identifiants de connexion

| Champ | Valeur |
|---|---|
| Nom d'utilisateur | **admin** |
| Mot de passe | **1234** |

---
## 🎬 Démonstration

▶️ **Voir la démo en vidéo** : https://drive.google.com/drive/folders/1_eAkSRziBxltB7C7D9u3HW2wcSKSYyWF?usp=sharing

---

## 👩‍💻 Auteur

**Ilef Falah** — 1ère année ingénieur Technologies Avancées  
ENSTAB — Université de Carthage  
Année universitaire : 2025/2026

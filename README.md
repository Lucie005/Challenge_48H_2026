# Y - Social | Réseau Social Ynov Campus

**Y - Social** est une plateforme communautaire interactive conçue pour les étudiants, intervenants et partenaires d'Ynov Campus. Elle permet de centraliser la communication, le partage de projets, la recherche de stages et l'entraide au sein d'un écosystème unique.

## 🚀 Fonctionnalités

### 👥 Communauté & Réseautage
- **Annuaire Global** : Recherchez des utilisateurs par nom, compétence ou promotion (B1, B2, B3, etc.).
- **Profils Polymorphiques** : Gestion de trois types de comptes : Étudiants, Staff/Intervenants et Entreprises Externes.
- **Système d'Amis** : Gestion des demandes d'ajouts, acceptations et liste d'amis dédiée.
- **Profil Personnalisable** : Édition de la biographie et gestion dynamique des compétences (système de tags).

### 📝 Fil d'Actualité & Interaction
- **Publications Multi-formats** : Partagez des posts classiques, des projets (🚀) ou des recherches de collaborateurs (🔍).
- **Interactions Sociales** : Système de "Like" et gestion des commentaires sous chaque publication.
- **Suppression** : Contrôle total sur vos propres publications.

### 💬 Messagerie & IA
- **Messagerie Instantanée** : Chat privé entre utilisateurs avec historique persistant.
- **Gestion des Demandes** : Onglet dédié dans la messagerie pour traiter les invitations reçues.
- **YnovBot IA** : Assistant intelligent propulsé par **OpenAI (GPT-3.5 Turbo)** pour répondre aux questions sur la vie du campus.

### 💼 Carrière & Organisation (YMatch)
- **Job Board** : Consultation d'offres de stages et d'alternances filtrables par type.
- **Emploi du Temps** : Visualisation des prochains cours (Mockup synchronisable via iCal).
- **News Ynov** : Flux d'actualités en temps réel spécifique au campus.

## 🛠️ Installation

### 1. Prérequis
- Python 3.9+
- Serveur MySQL (XAMPP, WAMP ou MySQL Server)

### 2. Configuration de la base de données
1. Créez une base de données nommée `ynov_social` dans votre interface (phpMyAdmin).
2. Importez le fichier `ynov_social.sql` fourni à la racine du projet.

### 3. Installation des dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration des variables d'environnement
Créez un fichier `.env` à la racine du projet :
```env
DATABASE_URL=mysql+pymysql://root:Admin123!@localhost/ynov_social
OPENAI_API_KEY=votre_cle_openai_ici
SECRET_KEY=votre_cle_secrete_flask
```
*Note : Si votre utilisateur MySQL `root` n'a pas de mot de passe, utilisez `root:@localhost`.*

## 🖥️ Utilisation

Lancez l'application avec la commande :
```bash
python app.py
```
L'application sera accessible sur `http://localhost:5000`.

### Comptes de test (SQL Dump)
- **Admin** : `admin@ynov.com` / `Admin123!`
- **Étudiant** : `axel@ynov.com` / `hash123` (Auto-haché au premier lancement)

## 🧪 Tests
Pour vérifier la connexion à la base de données :
```bash
python test.py
```

## 🏗️ Architecture Technique
- **Backend** : Flask (Python)
- **ORM** : SQLAlchemy
- **IA** : OpenAI API (Modèle gpt-3.5-turbo)
- **Frontend** : Jinja2, HTML5, CSS3 (Flexbox/Grid), JavaScript (Fetch API)
- **Authentification** : Werkzeug Security (Hachage scrypt)

---
*Projet développé dans le cadre du Challenge 48H 2026 - Paris Ynov Campus.*
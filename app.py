from flask import Flask, request, session, redirect, url_for, render_template
from modeles import db, User, Student, StaffYnov, ExternalUser, Message
import os

app = Flask(__name__)

# --- CONFIGURATION MYSQL ---
# Remplace 'root', 'ton_mdp' et 'ynov_social' par tes vrais identifiants MySQL
DB_USER = ""
DB_PASSWORD = ""
DB_HOST = ""
DB_NAME = ""

# On utilise mysql+pymysql pour la compatibilité avec SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key_48h')

# Initialisation de la base de données avec Flask
db.init_app(app)

with app.app_context():
    # Crée automatiquement les tables dans MySQL si elles n'existent pas encore
    db.create_all()
    
    # Création du compte admin personnalisé si inexistant
    if not User.query.filter_by(username='admin').first():
        admin = StaffYnov(
            username='admin',
            email='admin@ynov.com',
            role_title='Administrateur Principal'
        )
        admin.set_password('Admin123!')
        admin.can_moderate = True  # L'admin possède les droits par défaut
        db.session.add(admin)
        db.session.commit()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    data = request.form
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('user_type')

    # 1. Vérifier si l'utilisateur existe déjà
    if User.query.filter((User.email == email) | (User.username == username)).first():
        return "Email ou nom d'utilisateur déjà utilisé", 400

    # 2. Créer le bon type d'objet selon le choix du formulaire
    if user_type == 'student':
        new_user = Student(
            username=username,
            email=email,
            filiere=data.get('filiere'),
            skills=data.get('skills'),
            is_searching_job='is_searching_job' in data,
            Edt=data.get('Edt'),
            bio=data.get('bio')
        )
    elif user_type == 'staff':
        new_user = StaffYnov(
            username=username,
            email=email,
            role_title=data.get('role_title')
        )
    elif user_type == 'external':
        new_user = ExternalUser(
            username=username,
            email=email,
            organization=data.get('organization'),
            description=data.get('description')
        )
    else:
        return "Type d'utilisateur invalide", 400

    # 3. Hachage sécurisé via ta méthode de classe
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    
    # Si c'est un staff qui demande la modération, on envoie un message à l'admin
    if user_type == 'staff' and 'request_moderation' in data:
        admin_account = User.query.filter_by(username='admin').first()
        if admin_account:
            demande_msg = Message(
                sender_id=new_user.id,
                receiver_id=admin_account.id,
                body=f"L'utilisateur {new_user.username} souhaite obtenir les droits de modération."
            )
            db.session.add(demande_msg)
            db.session.commit()

    return "Inscription réussie !"

@app.route('/login', methods=['POST'])
def login():
    data = request.form
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    # Vérification : l'utilisateur existe ET le hash correspond
    if user and user.check_password(password):
        # Stockage en session
        session['user_id'] = user.id
        session['username'] = user.username
        session['user_type'] = user.user_type
        return f"Bienvenue {user.username} !"
    
    return "Email ou mot de passe incorrect", 401

@app.route('/logout')
def logout():
    session.clear()
    return "Déconnexion réussie !"

@app.route('/')
def home():
    return "Serveur Flask actif et connecté à MySQL !"

if __name__ == '__main__':
    app.run(debug=True)

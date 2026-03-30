from flask import Flask, request, session, redirect, url_for, render_template
from modeles import db, User, Student, StaffYnov, ExternalUser, Message
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)

# --- CONFIGURATION MYSQL CORRIGÉE ---
# Utilisation de 127.0.0.1 (plus stable) et du port 3306 vu sur ton image Workbench
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Admin123!@127.0.0.1:3306/ynov_social'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key_48h')

# Initialisation de la base
db.init_app(app)

with app.app_context():
    # On vérifie si l'admin existe déjà par son USERNAME ou son EMAIL
    admin_exists = User.query.filter((User.username == 'admin') | (User.email == 'admin@ynov.com')).first()
    
    if not admin_exists:
        print("Création du compte admin...")
        admin = StaffYnov(
            username='admin',
            email='admin@ynov.com',
            role_title='Administrateur Principal',
            user_type='staff'
        )
        admin.set_password('Admin123!')
        db.session.add(admin)
        db.session.commit()
    else:
        print("Le compte admin existe déjà, on passe à la suite.")

# --- ROUTES ---

@app.route('/')
def home():
    return "Serveur Flask actif et connecté à MySQL ! Allez sur /register pour tester."

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
    try:
        if user_type == 'student':
            new_user = Student(
                username=username,
                email=email,
                filiere=data.get('filiere'),
                bio=data.get('bio')
            )
        elif user_type == 'staff':
            new_user = StaffYnov(
                username=username,
                email=email,
                role_title=data.get('role_title')
            )
        else:
            new_user = ExternalUser(
                username=username,
                email=email,
                organization=data.get('organization')
            )

        # 3. Hachage du mot de passe
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        return "Inscription réussie ! Vous pouvez maintenant vérifier dans MySQL Workbench."

    except Exception as e:
        db.session.rollback()
        return f"Erreur lors de l'inscription : {e}", 500
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html') # Assure-toi d'avoir ce fichier

    data = request.form
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        session['user_id'] = user.id
        session['username'] = user.username
        session['user_type'] = user.user_type
        return f"Bienvenue {user.username} !"
    
    return "Email ou mot de passe incorrect", 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
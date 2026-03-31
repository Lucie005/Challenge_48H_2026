from modeles import db, User, Student, StaffYnov, ExternalUser, Message, Post
from flask import Flask, request, session, redirect, url_for, render_template, jsonify
from werkzeug.security import generate_password_hash
import os
import google.generativeai as genai
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURATION MYSQL CORRIGÉE ---
# Utilisation de 127.0.0.1 (plus stable) et du port 3306 vu sur ton image Workbench
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Admin123!@127.0.0.1:3306/ynov_social'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key_48h')

# Configuration Gemini AI
genai.configure(api_key=os.environ.get('GEMINI_API_KEY', 'VOTRE_CLE_API'))
ai_model = genai.GenerativeModel('gemini-pro')

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
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Récupération des posts pour le feed
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    user = User.query.get(session['user_id'])
    
    # Mock pour les widgets (IA et EDT)
    return render_template('index.html', posts=posts, user=user)

@app.route('/auth')
def auth():
    return render_template('auth.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('auth.html', mode='register')

    data = request.form
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    user_type = data.get('user_type')
    campus_id = data.get('campus_id')

    if password != confirm_password:
        return "Les mots de passe ne correspondent pas", 400

    # 1. Vérifier si l'utilisateur existe déjà
    if User.query.filter((User.email == email) | (User.username == username)).first():
        return "Email ou nom d'utilisateur déjà utilisé", 400

    campus_id = int(campus_id) if campus_id and campus_id.isdigit() else None

    # 2. Créer le bon type d'objet selon le choix du formulaire
    try:
        if user_type == 'student':
            new_user = Student(
                username=username,
                email=email,
                campus_id=campus_id,
                filiere=data.get('filiere'),
                skills=data.get('skills'),
                is_searching_job=data.get('is_searching_job') == 'on',
                edt=data.get('edt'),
                bio=data.get('bio')
            )
        elif user_type == 'staff':
            new_user = StaffYnov(
                username=username,
                email=email,
                campus_id=campus_id,
                role_title=data.get('role_title'),
                can_moderate=data.get('request_moderation') == 'on'
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

        # 3. Hachage du mot de passe
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    except Exception as e:
        db.session.rollback()
        return f"Erreur lors de l'inscription : {e}", 500
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth.html', mode='login')

    data = request.form
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        session['user_id'] = user.id
        session['username'] = user.username
        session['user_type'] = user.user_type
        return redirect(url_for('home'))
    
    return "Email ou mot de passe incorrect", 401

@app.route('/profile')
def profile():
    if 'user_id' not in session: return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/students')
def students_directory():
    if 'user_id' not in session: return redirect(url_for('login'))
    students = Student.query.all()
    return render_template('student.html', students=students)

@app.route('/jobs')
def jobs():
    if 'user_id' not in session: return redirect(url_for('login'))
    # Mock data en attendant un modèle Job
    job_offers = [
        {"title": "Développeur Python", "company": "Ynov Tech", "type": "Alternance", "desc": "Recherche B3..."},
        {"title": "UI Designer", "company": "Creative Agency", "type": "Stage", "desc": "Stage 6 mois..."}
    ]
    return render_template('jobs.html', job_offers=job_offers)

@app.route('/messages')
def messages():
    if 'user_id' not in session: return redirect(url_for('login'))
    # On récupère les conversations simplifiées (à affiner selon ton schéma)
    conversations = Message.query.filter(
        (Message.sender_id == session['user_id']) | (Message.receiver_id == session['user_id'])
    ).all()
    return render_template('messages.html', conversations=conversations)

# --- API ENDPOINTS ---

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({"reply": "Je n'ai pas compris votre question."}), 400
    
    try:
        response = ai_model.generate_content(f"Tu es l'assistant de l'école Ynov. Réponds brièvement : {prompt}")
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "Désolé, je rencontre une erreur technique."}), 500

@app.route('/load_edt', methods=['POST'])
def load_edt():
    # Logique fictive pour l'EDT
    mock_edt = [
        {"start": "09:00", "summary": "Python Expert", "location": "B01"},
        {"start": "14:00", "summary": "UX Design", "location": "C12"}
    ]
    return jsonify({"events": mock_edt})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
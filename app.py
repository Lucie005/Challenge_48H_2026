from modeles import db, User, Student, StaffYnov, ExternalUser, Message, Post, JobOffer, NewsYnov, Like, Comment, Contact
from flask import Flask, request, session, redirect, url_for, render_template, jsonify, flash
from werkzeug.security import generate_password_hash
import os
import google.generativeai as genai
from datetime import datetime
from sqlalchemy import text

app = Flask(__name__)

### --- CONFIGURATION BASE DE DONNÉES ---
# Note : Si vous utilisez XAMPP/WAMP, le mot de passe est souvent vide ('root:')
# Si vous avez défini un mot de passe durant l'install, remplacez Admin123! par le vôtre.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:Admin123!@localhost/ynov_social')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key_48h')

# Configuration Gemini AI
GEMINI_KEY = os.environ.get('GEMINI_API_KEY')
if not GEMINI_KEY or GEMINI_KEY == 'VOTRE_CLE_API':
    print("⚠️ ATTENTION : GEMINI_API_KEY n'est pas configurée.")

genai.configure(api_key=GEMINI_KEY if GEMINI_KEY else "DUMMY_KEY")
ai_model = genai.GenerativeModel('gemini-pro')

# Initialisation de la base
db.init_app(app)

with app.app_context():
    try:
        # 1. Création/Mise à jour des tables
        db.create_all()

        # 2. AUTO-RÉPARATION : Synchronisation de la structure SQL avec les modèles Python
        try:
            # Correction : La table du SQL dump limite user_type à (student, staff). 
            # On l'élargit pour accepter 'external' défini dans modeles.py
            db.session.execute(text("ALTER TABLE users MODIFY COLUMN user_type VARCHAR(20)"))
            
            # Ajout des colonnes de filtrage pour les posts si elles manquent
            db.session.execute(text("ALTER TABLE posts ADD COLUMN is_projet TINYINT(1) DEFAULT 0"))
            db.session.execute(text("ALTER TABLE posts ADD COLUMN is_recherche TINYINT(1) DEFAULT 0"))
            
            # Correction Bio : On s'assure que la colonne est dans 'users' pour tout le monde
            db.session.execute(text("ALTER TABLE users ADD COLUMN bio TEXT"))
            db.session.commit()
        except Exception:
            db.session.rollback()

        # 3. Récupération ou création du compte admin (admin.ynov dans ton SQL)
        admin = User.query.filter((User.username == 'admin') | (User.username == 'admin.ynov') | (User.email == 'admin@ynov.com')).first()
        if not admin:
            admin = StaffYnov(username='admin', email='admin@ynov.com', role_title='Admin Principal')
            db.session.add(admin)

        admin.set_password('Admin123!')
        db.session.commit()
        print("✅ Serveur et Base de données prêts !")
    except Exception as e:
        print(f"❌ Erreur critique au démarrage : {e}")

# --- ROUTES ---

@app.route('/')
def home():
    # Filtrage des posts
    posts = []
    news = []
    f_type = request.args.get('filter', 'all')
    try:
        query = Post.query

        if f_type == 'projet':
            query = query.filter_by(is_projet=True)
        elif f_type == 'recherche':
            query = query.filter_by(is_recherche=True)
        elif f_type == 'post':
            query = query.filter_by(is_projet=False, is_recherche=False)

        posts = query.order_by(Post.timestamp.desc()).all()
        
        # On récupère aussi les news (nécessaire pour index.html)
        news = NewsYnov.query.order_by(NewsYnov.created_at.desc()).limit(3).all()
    except Exception as e:
        print(f"❌ Erreur lors du chargement des données : {e}")

    user = None
    try:
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
    except Exception:
        user = None
    
    return render_template('index.html', posts=posts, user=user, current_filter=f_type, news=news)

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
        return render_template('auth.html', mode='register', error="Les mots de passe ne correspondent pas")

    # 1. Vérifier si l'utilisateur existe déjà
    if User.query.filter((User.email == email) | (User.username == username)).first():
        return render_template('auth.html', mode='register', error="Email ou nom d'utilisateur déjà utilisé")

    campus_id = int(campus_id) if campus_id and campus_id.isdigit() else None

    # 2. Créer le bon type d'objet selon le choix du formulaire
    bio = data.get('bio')
    try:
        if user_type == 'student':
            new_user = Student(
                username=username, email=email, bio=bio,
                campus_id=campus_id,
                filiere=data.get('filiere'),
                skills=data.get('skills'),
                is_searching_job=data.get('is_searching_job') == 'on',
                edt=data.get('edt')
            )
        elif user_type == 'staff':
            new_user = StaffYnov(
                username=username, email=email, bio=bio,
                campus_id=campus_id,
                role_title=data.get('role_title'),
                can_moderate=data.get('request_moderation') == 'on'
            )
        elif user_type == 'external':
            new_user = ExternalUser(
                username=username, email=email, bio=bio,
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
        return render_template('auth.html', mode='register', error=f"Erreur d'inscription : {e}")
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth.html', mode='login')

    data = request.form
    identifier = data.get('email') # Peut contenir l'email ou le username
    password = data.get('password')

    try:
        # Recherche par email OU par username
        user = User.query.filter((User.email == identifier) | (User.username == identifier)).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['user_type'] = user.user_type
            return redirect(url_for('home'))

    except Exception as e:
        print(f"❌ Erreur lors de la tentative de connexion : {e}")
        return render_template('auth.html', mode='login', error="Erreur technique de base de données.")

    return render_template('auth.html', mode='login', error="Identifiant ou mot de passe incorrect")

@app.route('/profile')
@app.route('/profile/<int:user_id>')
def profile(user_id=None):
    if 'user_id' not in session: return redirect(url_for('login'))
    
    # Si pas d'ID, on prend celui de la session (notre profil)
    target_id = user_id if user_id else session['user_id']
    user = User.query.get_or_404(target_id)
    
    # On vérifie si c'est notre propre profil pour autoriser la modification
    is_own_profile = (target_id == session['user_id'])
    
    rel_status = None
    if not is_own_profile:
        # Vérification bidirectionnelle de la relation
        rel = Contact.query.filter(
            ((Contact.user_id == session['user_id']) & (Contact.contact_id == target_id)) |
            ((Contact.user_id == target_id) & (Contact.contact_id == session['user_id']))
        ).first()
        if rel: rel_status = rel.status
    
    return render_template('profile.html', user=user, is_own_profile=is_own_profile, rel_status=rel_status)

@app.route('/profile/update', methods=['POST'])
def update_profile():
    if 'user_id' not in session: return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    
    user.username = request.form.get('username')
    user.bio = request.form.get('bio')
    
    # Si c'est un étudiant, on met à jour les champs spécifiques
    if user.user_type == 'student':
        user.filiere = request.form.get('filiere')
        user.skills = request.form.get('skills')

    db.session.commit()
    session['username'] = user.username # On met à jour la session aussi
    flash("Profil mis à jour avec succès !")
    return redirect(url_for('profile'))

@app.route('/students')
def students_directory():
    if 'user_id' not in session: return redirect(url_for('login'))
    my_id = session['user_id']
    # On exclut soi-même de la liste
    students = Student.query.filter(Student.id != my_id).all()
    
    # Récupération de toutes les relations impliquant l'utilisateur (envoyées et reçues)
    my_relations = Contact.query.filter((Contact.user_id == my_id) | (Contact.contact_id == my_id)).all()
    
    contact_status = {}
    for r in my_relations:
        other_id = r.contact_id if r.user_id == my_id else r.user_id
        # On stocke le statut et si c'est nous qui avons initié (pour afficher "Répondre" ou "En attente")
        is_sender = (r.user_id == my_id)
        contact_status[other_id] = {'status': r.status, 'is_sender': is_sender, 'request_id': r.id}
    
    return render_template('student.html', students=students, contact_status=contact_status)

@app.route('/api/contact/add/<int:contact_id>', methods=['POST'])
def add_contact(contact_id):
    if 'user_id' not in session: return jsonify({"error": "Non connecté"}), 401
    my_id = session['user_id']
    
    if my_id == contact_id:
        return jsonify({"error": "Vous ne pouvez pas vous ajouter vous-même"}), 400
        
    # Vérifie si une relation existe déjà dans N'IMPORTE QUEL sens
    existing = Contact.query.filter(
        ((Contact.user_id == my_id) & (Contact.contact_id == contact_id)) |
        ((Contact.user_id == contact_id) & (Contact.contact_id == my_id))
    ).first()

    if existing:
        return jsonify({"error": "Une relation existe déjà"}), 400
        
    try:
        new_rel = Contact(user_id=my_id, contact_id=contact_id, status='pending')
        db.session.add(new_rel)
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/contact/accept/<int:request_id>', methods=['POST'])
def accept_contact(request_id):
    if 'user_id' not in session: return jsonify({"error": "Non connecté"}), 401
    
    # On ne peut accepter que si on est le destinataire de la demande
    rel = Contact.query.get_or_404(request_id)
    if rel.contact_id != session['user_id']:
        return jsonify({"error": "Action non autorisée"}), 403
        
    try:
        rel.status = 'accepted'
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/contact/decline/<int:request_id>', methods=['POST'])
def decline_contact(request_id):
    if 'user_id' not in session: return jsonify({"error": "Non connecté"}), 401
    
    rel = Contact.query.get_or_404(request_id)
    # On peut supprimer si on est l'expéditeur (annuler) ou le destinataire (refuser)
    if rel.user_id != session['user_id'] and rel.contact_id != session['user_id']:
        return jsonify({"error": "Action non autorisée"}), 403
        
    try:
        db.session.delete(rel)
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/jobs')
def jobs():
    if 'user_id' not in session: return redirect(url_for('login'))
    # Récupération des offres réelles depuis la DB
    job_offers = JobOffer.query.order_by(JobOffer.created_at.desc()).all()
    return render_template('jobs.html', job_offers=job_offers)

@app.route('/messages')
def messages():
    if 'user_id' not in session: return redirect(url_for('login'))
    my_id = session['user_id']
    
    # Récupérer les IDs des personnes avec qui on a déjà discuté
    partners_query = db.session.query(Message.sender_id).filter(Message.receiver_id == my_id).union(
        db.session.query(Message.receiver_id).filter(Message.sender_id == my_id)
    ).all()
    
    partner_ids = {p[0] for p in partners_query if p[0] != my_id}
    
    # Si on vient de cliquer sur "Message" depuis le profil d'un étudiant
    target_id = request.args.get('user_id', type=int)
    if target_id and target_id != my_id:
        partner_ids.add(target_id)

    contacts = User.query.filter(User.id.in_(partner_ids)).all()
    return render_template('messages.html', contacts=contacts, active_id=target_id)

@app.route('/api/messages/<int:other_id>')
def get_messages(other_id):
    if 'user_id' not in session: return jsonify([]), 401
    my_id = session['user_id']
    msgs = Message.query.filter(
        ((Message.sender_id == my_id) & (Message.receiver_id == other_id)) |
        ((Message.sender_id == other_id) & (Message.receiver_id == my_id))
    ).order_by(Message.sent_at.asc()).all()
    
    return jsonify([{
        "body": m.body,
        "is_mine": m.sender_id == my_id,
        "sent_at": m.sent_at.strftime('%H:%M')
    } for m in msgs])

@app.route('/api/messages/send', methods=['POST'])
def send_message():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    receiver_id = data.get('receiver_id')
    body = data.get('body')
    
    if not body or not receiver_id:
        return jsonify({"error": "Données manquantes"}), 400
        
    try:
        msg = Message(sender_id=session['user_id'], receiver_id=receiver_id, body=body)
        db.session.add(msg)
        db.session.commit()
        return jsonify({"success": True, "sent_at": msg.sent_at.strftime('%H:%M')})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/create_post', methods=['POST'])
def create_post():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    content = request.form.get('content')
    post_type = request.form.get('post_type')
    media_type = request.form.get('media_type')
    media_url = request.form.get('media_url')
    
    new_post = Post(
        author_id=session['user_id'],
        content=content,
        media_type=media_type,
        media_url=media_url if media_type != 'text' else None,
        is_projet=(post_type == 'projet'),
        is_recherche=(post_type == 'recherche')
    )
    
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('home'))

# --- API ENDPOINTS ---

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({"reply": "Je n'ai pas compris votre question."}), 400
    
    if not GEMINI_KEY or GEMINI_KEY == 'VOTRE_CLE_API':
        return jsonify({"reply": "L'IA n'est pas configurée. Veuillez définir la variable d'environnement GEMINI_API_KEY."}), 200

    try:
        response = ai_model.generate_content(f"Tu es l'assistant de l'école Ynov. Réponds brièvement : {prompt}")
        if response and response.text:
            return jsonify({"reply": response.text})
        return jsonify({"reply": "L'IA n'a pas pu générer de réponse."})
    except Exception as e:
        print(f"Erreur IA: {e}")
        return jsonify({"reply": "Désolé, je rencontre une erreur technique avec Gemini."}), 500

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
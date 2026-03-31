from modeles import db, User, Student, StaffYnov, ExternalUser, Message, Post, JobOffer, NewsYnov, Like, Comment, Contact, Notification
from flask import Flask, request, session, redirect, url_for, render_template, jsonify, flash
from werkzeug.security import generate_password_hash
import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy import text

app = Flask(__name__)
load_dotenv()

### --- CONFIGURATION BASE DE DONNÉES ---
# Note : Si vous utilisez XAMPP/WAMP, le mot de passe est souvent vide ('root:')
# Si vous avez défini un mot de passe durant l'install, remplacez Admin123! par le vôtre.
### Note: Sur XAMPP/WAMP, le mot de passe root est souvent vide. 
### Si la connexion échoue, essayez : 'mysql+pymysql://root:@localhost/ynov_social'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:Admin123!@localhost/ynov_social')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key_48h')

# Initialisation de la base
db.init_app(app)

with app.app_context():
    try:
        # 1. AUTO-RÉPARATION : On lance les ALTER TABLE en premier avec du SQL pur
        # pour éviter que SQLAlchemy ne plante en essayant de mapper des colonnes absentes
        commands = [
            "ALTER TABLE users MODIFY COLUMN user_type VARCHAR(20)",
            "ALTER TABLE posts ADD COLUMN is_projet TINYINT(1) DEFAULT 0",
            "ALTER TABLE posts ADD COLUMN is_recherche TINYINT(1) DEFAULT 0",
            "ALTER TABLE users ADD COLUMN bio TEXT",
            "ALTER TABLE users ADD COLUMN github_url VARCHAR(255)",
            "ALTER TABLE users ADD COLUMN linkedin_url VARCHAR(255)",
            "ALTER TABLE users ADD COLUMN portfolio_url VARCHAR(255)"
        ]
        for cmd in commands:
            try:
                db.session.execute(text(cmd))
                db.session.commit()
            except Exception as e:
                db.session.rollback()

        # 2. Création des tables manquantes via SQLAlchemy
        db.create_all()

        # 3. Réparation forcée du compte Admin pour garantir la connexion
        # On utilise une requête SQL brute pour éviter le crash si la colonne bio bug encore
        admin = User.query.filter((User.email == 'admin@ynov.com') | (User.username == 'admin.ynov')).first()
        if not admin:
            admin = StaffYnov(username='admin.ynov', email='admin@ynov.com', role_title='Admin Principal')
            db.session.add(admin)

        admin.set_password('Admin123!')
        db.session.commit()
        print("✅ Serveur et Base de données prêts !")
    except Exception as e:
        print(f"❌ Erreur critique au démarrage : {e}")

# --- HELPER POUR LA SÉCURITÉ ---
def check_auth():
    """Vérifie si l'utilisateur est connecté, sinon affiche l'écran de verrouillage."""
    if 'user_id' not in session:
        return render_template('unauthorized.html')
    return None

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

        if not user:
            print(f"⚠️ Tentative de connexion échouée : l'utilisateur '{identifier}' n'existe pas.")
        elif not user.check_password(password):
            print(f"⚠️ Mot de passe incorrect pour l'utilisateur : {identifier}")
        else:
            session['user_id'] = user.id
            session['username'] = user.username
            session['user_type'] = user.user_type
            print(f"✅ Connexion réussie : {user.username}")
            return redirect(url_for('home'))

    except Exception as e:
        print(f"❌ Erreur lors de la tentative de connexion : {e}")
        return render_template('auth.html', mode='login', error="Erreur technique de base de données.")

    return render_template('auth.html', mode='login', error="Identifiant ou mot de passe incorrect")

@app.route('/profile')
@app.route('/profile/<int:user_id>')
def profile(user_id=None):
    auth_check = check_auth()
    if auth_check: return auth_check
    
    # Priorité : argument URL -> paramètre query -> session
    target_id = user_id or request.args.get('user_id', type=int) or session.get('user_id')
    # On utilise db.session.query pour être sûr de récupérer l'objet polymorphique complet
    user = db.session.query(User).filter_by(id=target_id).first_or_404()
    
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
    # On utilise une requête filtrée pour garantir que l'objet polymorphique (Student/Staff) est bien chargé
    user = db.session.query(User).filter_by(id=session['user_id']).first()
    
    user.username = request.form.get('username')
    user.bio = request.form.get('bio')
    user.github_url = request.form.get('github_url')
    user.linkedin_url = request.form.get('linkedin_url')
    user.portfolio_url = request.form.get('portfolio_url')
    
    if user.user_type == 'student':
        user.filiere = request.form.get('filiere')
        user.skills = request.form.get('skills')
    elif user.user_type == 'staff':
        user.role_title = request.form.get('role_title')
    elif user.user_type == 'external':
        user.organization = request.form.get('organization')

    db.session.commit()
    session['username'] = user.username # On met à jour la session aussi
    flash("Profil mis à jour avec succès !")
    return redirect(url_for('profile'))

@app.route('/users', methods=['GET'])
def users_directory():
    auth_check = check_auth()
    if auth_check: return auth_check
    my_id = session['user_id']
    
    search_query = request.args.get('q', '')
    promo_filter = request.args.get('promo', 'all')
    
    # On récupère tous les types d'utilisateurs sauf soi-même
    query = User.query.filter(User.id != my_id)
    
    if search_query:
        query = query.filter(User.username.contains(search_query))
    if promo_filter != 'all' and hasattr(Student, 'filiere'):
        query = query.filter(Student.filiere.contains(promo_filter))
        
    users = query.all()
    
    # Récupération de toutes les relations impliquant l'utilisateur (envoyées et reçues)
    my_relations = db.session.query(Contact).filter((Contact.user_id == my_id) | (Contact.contact_id == my_id)).all()
    
    contact_status = {}
    for r in my_relations:
        other_id = r.contact_id if r.user_id == my_id else r.user_id
        # On stocke le statut et l'expéditeur
        is_sender = (r.user_id == my_id)
        contact_status[other_id] = {'status': r.status, 'is_sender': is_sender, 'request_id': r.id}
    
    return render_template('student.html', users=users, contact_status=contact_status)

@app.route('/friends')
def friends_page():
    auth_check = check_auth()
    if auth_check: return auth_check
    my_id = session['user_id']

    # Récupérer uniquement les amis acceptés
    friends_query = Contact.query.filter(
        ((Contact.user_id == my_id) | (Contact.contact_id == my_id)),
        Contact.status == 'accepted'
    ).all()
    friends = [f.receiver if f.user_id == my_id else f.requester for f in friends_query]

    return render_template('friends.html', friends=friends)

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
    auth_check = check_auth()
    if auth_check: return auth_check

    j_type = request.args.get('type', 'all')
    query = JobOffer.query
    if j_type != 'all':
        query = query.filter_by(type=j_type)
        
    job_offers = query.order_by(JobOffer.created_at.desc()).all()
    return render_template('jobs.html', job_offers=job_offers, current_type=j_type)

@app.route('/messages')
def messages():
    auth_check = check_auth()
    if auth_check: return auth_check
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

    # Récupérer les demandes d'amis reçues en attente
    pending_requests = Contact.query.filter_by(contact_id=my_id, status='pending').all()

    active_user = User.query.get(target_id) if target_id else None
    contacts = User.query.filter(User.id.in_(partner_ids)).all()
    return render_template('messages.html', contacts=contacts, active_id=target_id, active_user=active_user, pending_requests=pending_requests)

@app.route('/api/messages/<int:other_id>')
def get_messages(other_id):
    if 'user_id' not in session: return jsonify([]), 401
    my_id = session['user_id']
    
    query = Message.query.filter(
        ((Message.sender_id == my_id) & (Message.receiver_id == other_id)) |
        ((Message.sender_id == other_id) & (Message.receiver_id == my_id))
    )
    
    # Marquer comme lu les messages reçus
    unread = query.filter(Message.receiver_id == my_id, Message.is_read == False).all()
    for m in unread: m.is_read = True
    db.session.commit()
    
    msgs = query.order_by(Message.sent_at.asc()).all()
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

@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if 'user_id' not in session: return redirect(url_for('login'))
    post = Post.query.get_or_404(post_id)
    
    if post.author_id != session['user_id']:
        flash("Action non autorisée.")
        return redirect(url_for('home'))
        
    try:
        db.session.delete(post)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        
    return redirect(request.referrer or url_for('home'))

@app.route('/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    if 'user_id' not in session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"error": "Unauthorized"}), 401
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    existing_like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
    if existing_like:
        db.session.delete(existing_like)
    else:
        new_like = Like(user_id=user_id, post_id=post_id)
        db.session.add(new_like)
    db.session.commit()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({"success": True, "count": Post.query.get(post_id).likes_count})
    return redirect(request.referrer or url_for('home'))

@app.route('/comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    if 'user_id' not in session: return redirect(url_for('login'))
    contenu = request.form.get('contenu')
    if contenu:
        comment = Comment(post_id=post_id, user_id=session['user_id'], contenu=contenu)
        db.session.add(comment)
        db.session.commit()
    return redirect(request.referrer or url_for('home'))

# --- API ENDPOINTS ---

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({"reply": "Je n'ai pas compris votre question."}), 400
    
    # Configuration OpenAI (Priorité à l'environnement, sinon utilise la clé fournie)
    api_key = os.environ.get('OPENAI_API_KEY') or "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"

    if not api_key:
        return jsonify({"reply": "L'IA n'est pas configurée."}), 200

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es l'assistant de l'école Ynov. Réponds brièvement."},
                {"role": "user", "content": prompt}
            ]
        )
        return jsonify({"reply": response.choices[0].message.content})
    except Exception as e:
        print(f"Erreur IA: {e}")
        return jsonify({"reply": f"Désolé, je rencontre une erreur technique avec l'IA : {str(e)}"}), 500

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
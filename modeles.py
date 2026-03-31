from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# --- CLASSE MÈRE ---
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    photo = db.Column(db.String(255))
    password_hash = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Système d'héritage (Polymorphisme)
    user_type = db.Column(db.String(20), nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': user_type
    }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_avatar(self):
        return f"https://ui-avatars.com/api/?name={self.username}&background=random"

    @property
    def followers_count(self):
        return db.session.query(db.func.count()).filter(Follow.following_id == self.id).scalar()

    @property
    def following_count(self):
        return db.session.query(db.func.count()).filter(Follow.follower_id == self.id).scalar()
    
class Campus(db.Model):
    __tablename__ = 'campus'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    ville = db.Column(db.String(100), nullable=False)
    pays = db.Column(db.String(100), default='France')

# --- CLASSES FILLES ---
class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    campus_id = db.Column(db.Integer, db.ForeignKey('campus.id'))
    filiere = db.Column(db.String(50))
    skills = db.Column(db.Text)
    is_searching_job = db.Column(db.Boolean, default=False)
    edt = db.Column(db.String(100))

    __mapper_args__ = {'polymorphic_identity': 'student'}

class StaffYnov(User):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    campus_id = db.Column(db.Integer, db.ForeignKey('campus.id'))
    role_title = db.Column(db.String(100))
    can_moderate = db.Column(db.Boolean, default=False)

    __mapper_args__ = {'polymorphic_identity': 'staff'}

class ExternalUser(User):
    __tablename__ = 'external_user' 
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    organization = db.Column(db.String(100)) # Entreprise ou asso si il y en a une
    description = db.Column(db.String(255)) # Pourquoi ils sont là

    __mapper_args__ = {'polymorphic_identity': 'external'}

class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    following_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

class JobOffer(db.Model):
    __tablename__ = 'job_offers'
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    entreprise = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.Enum('stage', 'alternance', 'CDI', 'CDD'), nullable=False)
    lieu = db.Column(db.String(200))
    duree = db.Column(db.String(100))
    lien = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now)

class NewsYnov(db.Model):
    __tablename__ = 'news_ynov'
    id = db.Column(db.Integer, primary_key=True)
    campus_id = db.Column(db.Integer, db.ForeignKey('campus.id'))
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    date_event = db.Column(db.Date)
    categorie = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now)

class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Enum('pending', 'accepted'), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.now)

# --- AUTRES CLASSES ---
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text)
    media_url = db.Column(db.String(255))
    media_type = db.Column(db.String(20), default='text') # text, image, video
    is_reel = db.Column(db.Boolean, default=False)
    is_projet = db.Column(db.Boolean, default=False)
    is_recherche = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, name='created_at')
    author = db.relationship('User', backref='posts', foreign_keys=[author_id])

    @property
    def likes_count(self):
        return db.session.query(db.func.count(Like.id)).filter(Like.post_id == self.id).scalar()

    @property
    def comments_count(self):
        return db.session.query(db.func.count(Comment.id)).filter(Comment.post_id == self.id).scalar()

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    sent_at = db.Column(db.DateTime, default=datetime.now)

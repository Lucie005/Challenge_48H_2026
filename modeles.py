from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# --- CLASSE MÈRE ---
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Système d'héritage (Polymorphisme)
    user_type = db.Column(db.String(20), nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': user_type
    }

    def set_password(self, password):
        self._password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password_hash, password)

    def get_avatar(self):
        return f"https://ui-avatars.com/api/?name={self.username}&background=random"

# --- CLASSES FILLES ---
class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    filiere = db.Column(db.String(50))
    skills = db.Column(db.Text)
    is_searching_job = db.Column(db.Boolean, default=False)
    Edt = db.Column(db.String(100))
    bio = db.Column(db.Text)

    __mapper_args__ = {'polymorphic_identity': 'student'}

class StaffYnov(User):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role_title = db.Column(db.String(100))
    can_moderate = db.Column(db.Boolean, default=True)

    __mapper_args__ = {'polymorphic_identity': 'staff'}

class ExternalUser(User):
    __tablename__ = 'external_user' 
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    organization = db.Column(db.String(100)) # Entreprise ou asso si il y en a une
    description = db.Column(db.String(255)) # Pourquoi ils sont là

    __mapper_args__ = {'polymorphic_identity': 'external'}

# --- AUTRES CLASSES ---
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text)
    media_url = db.Column(db.String(255))
    media_type = db.Column(db.String(20), default='text') # text, image, video
    is_reel = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.relationship('User', backref='posts')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

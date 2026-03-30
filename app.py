from flask import Flask
from modeles import db
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

@app.route('/')
def home():
    return "Serveur Flask actif et connecté à MySQL !"

if __name__ == '__main__':
    app.run(debug=True)

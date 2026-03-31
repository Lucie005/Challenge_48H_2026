from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# CONFIGURATION (Vérifie bien le nom de la base 'ynov_social')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Admin123!@localhost/ynov_social'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# On définit un modèle minimal juste pour le test
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))

def test_connection():
    with app.app_context():
        try:
            # On tente de récupérer le premier utilisateur de ta table
            first_user = User.query.first()
            if first_user:
                print(f"✅ Connexion réussie ! Premier utilisateur trouvé : {first_user.username}")
            else:
                print("⚠️ Connexion OK, mais la table 'users' est vide.")
        except Exception as e:
            print(f"❌ Erreur de connexion : {e}")

if __name__ == "__main__":
    test_connection()
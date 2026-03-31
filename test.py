from app import app, db
from modeles import User

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
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Inscription - Ynov Social</title>
    <style>
        body { font-family: sans-serif; background: #f4f7f6; display: flex; justify-content: center; padding: 20px; }
        .container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 400px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; font-weight: bold; margin-bottom: 5px; }
        input, select, textarea { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
        .hidden { display: none; }
        button { width: 100%; padding: 12px; background: #0056b3; color: white; border: none; cursor: pointer; border-radius: 4px; }
        .dynamic-section { background: #f9f9f9; padding: 10px; border-left: 3px solid #0056b3; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Créer un compte</h2>
        <form action="/register" method="POST">
            <div class="form-group">
                <label>Pseudo</label>
                <input type="text" name="username" required>
            </div>
            <div class="form-group">
                <label>Email</label>
                <input type="email" name="email" required>
            </div>
            <div class="form-group">
                <label>Mot de passe</label>
                <input type="password" name="password" required>
            </div>
            <div class="form-group">
                <label>Je suis :</label>
                <select id="user_type" name="user_type" onchange="toggleFields()">
                    <option value="student">Étudiant</option>
                    <option value="staff">Staff Ynov</option>
                    <option value="external">Externe</option>
                </select>
            </div>

            <div id="student_fields" class="dynamic-section">
                <label>Filière</label>
                <input type="text" name="filiere" placeholder="B2 Informatique...">
                <label>Bio</label>
                <textarea name="bio"></textarea>
            </div>

            <div id="staff_fields" class="dynamic-section hidden">
                <label>Titre / Poste</label>
                <input type="text" name="role_title">
            </div>

            <div id="external_fields" class="dynamic-section hidden">
                <label>Entreprise</label>
                <input type="text" name="organization">
            </div>

            <button type="submit">S'inscrire</button>
        </form>
    </div>

    <script>
        function toggleFields() {
            const type = document.getElementById('user_type').value;
            document.getElementById('student_fields').classList.add('hidden');
            document.getElementById('staff_fields').classList.add('hidden');
            document.getElementById('external_fields').classList.add('hidden');
            document.getElementById(type + '_fields').classList.remove('hidden');
        }
    </script>
</body>
</html>
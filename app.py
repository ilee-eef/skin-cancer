from flask import Flask, render_template, request, redirect, session, flash
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import mysql.connector
from mysql.connector import Error
import os
import uuid

app = Flask(__name__)
app.secret_key = 'skin_cancer_secret_2026'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def get_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='skin_cancer_db'
    )

try:
    model = load_model('model/vgg16_malignant_benign.h5')
    print("✓ Modèle chargé avec succès")
except Exception as e:
    print(f"✗ Erreur chargement modèle: {e}")
    model = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def secure_unique_filename(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    return f"{uuid.uuid4().hex}.{ext}"


@app.route('/', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect('/dashboard')
    if request.method == 'POST':
        user = request.form['username'].strip()
        pwd = request.form['password']
        try:
            db = get_db()
            cursor = db.cursor(dictionary=True)
            cursor.execute(
                'SELECT * FROM users WHERE username=%s AND password=%s',
                (user, pwd)
            )
            result = cursor.fetchone()
            db.close()
            if result:
                session['user'] = user
                return redirect('/dashboard')
            else:
                flash('Nom d\'utilisateur ou mot de passe incorrect', 'danger')
        except Error as e:
            flash(f'Erreur base de données: {e}', 'danger')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        confirm = request.form['confirm']

        if password != confirm:
            flash('Les mots de passe ne correspondent pas', 'danger')
            return redirect('/register')

        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute('SELECT * FROM users WHERE username=%s', (username,))
            existing = cursor.fetchone()
            if existing:
                flash('Ce nom d\'utilisateur existe déjà', 'danger')
                db.close()
                return redirect('/register')
            cursor.execute(
                'INSERT INTO users (username, password) VALUES (%s, %s)',
                (username, password)
            )
            db.commit()
            db.close()
            flash('Compte créé avec succès ! Connectez-vous.', 'success')
            return redirect('/')
        except Error as e:
            flash(f'Erreur: {e}', 'danger')

    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template('dashboard.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'user' not in session:
        return redirect('/')

    if request.method == 'POST':
        if model is None:
            flash('Modèle IA non disponible', 'danger')
            return redirect('/predict')

        name = request.form.get('name', '').strip()
        age = request.form.get('age', '').strip()
        file = request.files.get('image')

        if not name or not age:
            flash('Veuillez remplir tous les champs', 'warning')
            return redirect('/predict')

        if not file or file.filename == '':
            flash('Veuillez choisir une image', 'warning')
            return redirect('/predict')

        if not allowed_file(file.filename):
            flash('Format non supporté. Utilisez JPG ou PNG', 'warning')
            return redirect('/predict')

        try:
            filename = secure_unique_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(path)

            img = image.load_img(path, target_size=(224, 224))
            img_array = image.img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            pred = model.predict(img_array)[0][0]
            result = 'Malignant' if pred > 0.5 else 'Benign'
            prob = round(float(pred) * 100, 2)

            db = get_db()
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO patients (name, age, result, probability, image_path)
                VALUES (%s, %s, %s, %s, %s)""",
                (name, int(age), result, float(pred), path)
            )
            db.commit()
            db.close()

            return render_template('result.html',
                result=result,
                prob=prob,
                img=path,
                name=name,
                age=age
            )

        except Exception as e:
            flash(f'Erreur lors de l\'analyse: {e}', 'danger')
            return redirect('/predict')

    return render_template('predict.html')


@app.route('/patients')
def patients():
    if 'user' not in session:
        return redirect('/')
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM patients ORDER BY created_at DESC')
        data = cursor.fetchall()
        db.close()
    except Error as e:
        flash(f'Erreur: {e}', 'danger')
        data = []
    return render_template('patients.html', patients=data)


@app.route('/delete/<int:id>')
def delete(id):
    if 'user' not in session:
        return redirect('/')
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM patients WHERE id=%s', (id,))
        db.commit()
        db.close()
        flash('Patient supprimé avec succès', 'success')
    except Error as e:
        flash(f'Erreur: {e}', 'danger')
    return redirect('/patients')


@app.route('/logout')
def logout():
    session.clear()
    flash('Déconnecté avec succès', 'info')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
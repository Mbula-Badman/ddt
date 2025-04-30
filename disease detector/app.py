from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for sessions

# Dummy database (for now; later you can connect MySQL)
USERS = {}  # Will store users like {'username': 'password'}

# Landing Page
@app.route('/landing')
def landing():
    return render_template('landing.html')

# Home/Login Page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USERS and USERS[username] == password:
            session['user'] = username
            return redirect(url_for('symptoms'))
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')

# Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USERS:
            return "Username already exists. Please choose a different one."
        USERS[username] = password
        return redirect(url_for('login'))
    return render_template('register.html')

# Symptoms Checker Page
@app.route('/symptoms', methods=['GET', 'POST'])
def symptoms():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        symptoms_input = request.form.get('symptoms', '').lower()
        # Simple keyword-based "prediction"
        if 'cough' in symptoms_input:
            disease = 'Tuberculosis'
        elif 'fever' in symptoms_input:
            disease = 'HIV'
        elif 'headache' in symptoms_input:
            disease = 'High Blood Pressure'
        elif 'stomach' in symptoms_input:
            disease = 'Stomach Ulcer'
        else:
            disease = 'Unknown'
        return render_template('result.html', disease=disease)
    return render_template('symptoms.html')

# Logout Route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

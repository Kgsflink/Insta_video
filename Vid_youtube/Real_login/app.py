
import argparse
from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = "d20d5a8e7caee1a454f61cbb44945cd4"

# Check if config file exists, if not create it
CONFIG_FILE = "config.json"
if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w") as f:
        json.dump({}, f)

# Load user data from config file
with open(CONFIG_FILE, "r") as f:
    users = json.load(f)

# Route for the homepage
@app.route('/')
def index():
    if 'email' in session:
        logged_in = True
    else:
        logged_in = False
    return render_template('index.html', logged_in=logged_in)

# Route for the sign-up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password == confirm_password:
            users[email] = {'name': name, 'password': password}
            with open(CONFIG_FILE, "w") as f:
                json.dump(users, f)
            session['email'] = email
            session['name'] = name
            return redirect(url_for('dashboard'))
        else:
            return "Passwords do not match"
    return render_template('signup.html')

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email]['password'] == password:
            session['email'] = email
            session['name'] = users[email]['name']
            return redirect(url_for('dashboard'))
        else:
            return "Invalid email or password"
    return render_template('login.html')

# Route for the dashboard
@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        name = session['name']
        email = session['email']
        return render_template('dashboard.html', name=name, email=email)
    else:
        return redirect(url_for('login'))

# Route for logging out
@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('name', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5000, help="Port number")
    args = parser.parse_args()
    app.run(debug=True, host='0.0.0.0', port=args.port)

from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///review_system.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Database Models
class Reviewer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    expertise = db.Column(db.String(200))
    availability = db.Column(db.Boolean, default=True)

class ResearchPaper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    abstract = db.Column(db.Text)
    keywords = db.Column(db.String(200))
    assigned_reviewers = db.Column(db.String(200))

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Reviewer.query.filter_by(email=email).first()
        admin = Admin.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_type'] = 'reviewer'
            return redirect(url_for('reviewer_dashboard'))
        elif admin and check_password_hash(admin.password, password):
            session['user_id'] = admin.id
            session['user_type'] = 'admin'
            return redirect(url_for('admin_dashboard'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' in session and session['user_type'] == 'admin':
        papers = ResearchPaper.query.all()
        reviewers = Reviewer.query.all()
        return render_template('admin_dashboard.html', papers=papers, reviewers=reviewers)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_type', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)


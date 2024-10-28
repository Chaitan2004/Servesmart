from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import segno
import uuid
import os
import datetime
import base64
from io import BytesIO

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # Secret key for sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/servesmart'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

db = SQLAlchemy(app)

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    type = db.Column(db.String(9), unique=False, nullable=False)


class Meals(db.Model):
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), db.ForeignKey('users.username'), nullable=False, index=True)  # Indexed foreign key
    qrcode = db.Column(db.LargeBinary, nullable=False)
    meal_type = db.Column(db.String(50), nullable=False)  # e.g., "breakfast" or "dinner"
    date = db.Column(db.Date, nullable=False, index=True)  # Index for efficient date filtering

    user = db.relationship('users', backref=db.backref('meals', lazy=True))

def b64encode(data):
    return base64.b64encode(data).decode('utf-8')

app.jinja_env.filters['b64encode'] = b64encode

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    password = request.form['password']

    if username and password:
        # Check if the user exists in the database
        user = users.query.filter_by(username=username, password=password).first()
        if user:
            # Store the username and user type in the session
            session['username'] = user.username
            session['type'] = user.type
            session['cards'] = 5  # Example: set initial tokens for the user; replace this logic as needed

            if user.type == 'admin':
                return redirect('/admin-dashboard')
            else:
                return redirect('/student-dashboard')
        else:
            return "Invalid credentials. Please try again."
    else:
        return "Please provide both username and password."

@app.route('/admin-dashboard')
def admin_dashboard():
    return "Welcome to the Admin Dashboard!"

@app.route('/student-dashboard')
def student_dashboard():
    # Check if the user is logged in (i.e., 'username' is in the session)
    if 'username' not in session:
        # If not logged in, redirect to the login page
        return redirect(url_for('index'))
    # If logged in, render the student dashboard
    return render_template('studentdashboard.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('studentdashboard.html')

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    # Redirect the user back to the login page
    return redirect(url_for('index'))

@app.route('/commondininghall')
def commondininghall():
    # Check if the user is logged in (i.e., 'username' is in the session)
    if 'username' not in session:
        # If not logged in, redirect to the login page
        return redirect(url_for('index'))
    # If logged in, render the student dashboard
    return render_template('commondininghall.html')


@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    meal_type = request.form.get('meal')  # e.g., "breakfast" or "dinner"
    username = session.get('username')  # Use username from session

    if meal_type and username:
        # Generate a unique QR code
        unique_id = str(uuid.uuid4())
        qr = segno.make(unique_id)
        img_buffer = BytesIO()
        qr.save(img_buffer, kind='png', scale=10)  # Increase scale for higher resolution
        img_binary = img_buffer.getvalue()

        # Insert new meal record for the student
        new_meal = Meals(username=username, qrcode=img_binary, meal_type=meal_type, date=datetime.date.today())
        db.session.add(new_meal)
        db.session.commit()

    return render_template('commondininghall.html', qr_generated=True, meal_type=meal_type)

@app.route('/generated_qrs')
def generated_qrs():
    if 'username' not in session:
        return redirect(url_for('index'))

    # Fetch all generated QR codes for the logged-in user from the database
    username = session['username']
    qr_codes = Meals.query.filter_by(username=username).all()

    return render_template('generated_qrs.html', qr_codes=qr_codes)



if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import segno
import uuid
import os
from datetime import datetime, timedelta, time
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
    current_date = datetime.today().date()
    date_options = [
        current_date,
        current_date + timedelta(days=1),
        current_date + timedelta(days=2)
    ]
    return render_template('commondininghall.html', current_date=current_date, date_options=date_options)
@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    meal = request.form.get('meal')
    meal_date = request.form.get('meal_date')
    username = session.get('username')
    qr_generated = False

    # Convert the selected meal_date to a datetime object
    meal_date_obj = datetime.strptime(meal_date, "%Y-%m-%d").date() if meal_date else None
    if not meal_date_obj:
        flash("Please select a valid date.", "error")
        return redirect(url_for('commondininghall'))

    # Define meal times
    lunch_time = time(12, 0)  # 12:00 PM
    dinner_time = time(19, 0)  # 7:00 PM
    current_time = datetime.now()

    # Ensure the selected date is within the next two days
    if meal_date_obj > current_time.date() + timedelta(days=2):
        flash("QR code generation is only available up to two days in advance.", "error")
        return redirect(url_for('commondininghall'))

    # Calculate cut-off times for QR code generation
    if meal == 'lunch':
        cutoff_time = datetime.combine(meal_date_obj, lunch_time) - timedelta(hours=4)
    elif meal == 'dinner':
        cutoff_time = datetime.combine(meal_date_obj, dinner_time) - timedelta(hours=4)
    else:
        flash("Invalid meal type.", "error")
        return redirect(url_for('commondininghall'))

    # Restrict QR generation if past the cut-off time
    if current_time > cutoff_time:
        flash(f"QR code generation for {meal} on {meal_date} is closed.", "error")
        return redirect(url_for('commondininghall'))

    # Check if a QR code has already been generated for this meal and date
    existing_meal = Meals.query.filter_by(username=username, meal_type=meal, date=meal_date_obj).first()
    if existing_meal:
        flash("You have already generated a QR code for this meal on the selected date.", "error")
        return redirect(url_for('commondininghall'))

    # Proceed if within the allowed time and date
    if meal and username:
        unique_id = str(uuid.uuid4())
        qr = segno.make(unique_id)
        img_buffer = BytesIO()
        qr.save(img_buffer, kind='png', scale=10)
        img_binary = img_buffer.getvalue()

        new_meal = Meals(username=username, qrcode=img_binary, meal_type=meal, date=meal_date_obj)
        db.session.add(new_meal)
        db.session.commit()

        qr_generated = True
        session['qr_generated'] = qr_generated
        session['meal'] = meal

    # Clear session qr_generated status for fresh submission capability
    session.pop('qr_generated', None)

    current_date = datetime.today().date()
    date_options = [
        current_date,
        current_date + timedelta(days=1),
        current_date + timedelta(days=2)
    ]

    # Pass current date to avoid shrinking of date options on reload
    return render_template('commondininghall.html', qr_generated=qr_generated, meal=meal, current_date=current_time.date(), date_options=date_options)
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
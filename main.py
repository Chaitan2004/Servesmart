from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import segno
import uuid
import os
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
    qrcode = db.Column(db.LargeBinary, nullable=False)  # Store image as binary (LONGBLOB)

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
    qr_generated = False
    meal = None

    if request.method == 'POST':
        meal = request.form.get('meal')

        if meal:
            # Generate unique identifier
            unique_id = str(uuid.uuid4())

            # Generate QR code using segno
            qr = segno.make(unique_id)

            # Save the QR code as PNG to BytesIO
            img_buffer = BytesIO()
            qr.save(img_buffer, kind='png')
            img_binary = img_buffer.getvalue()

            # Store unique ID, meal type, and image data in the database
            new_qr = users(qrcode=img_binary)
            db.session.add(new_qr)
            db.session.commit()

            qr_generated = True

    return render_template('commondininghall.html', qr_generated=qr_generated, meal=meal)


if __name__ == '__main__':
    app.run(debug=True)
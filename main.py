from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid
import os
from datetime import datetime, timedelta, time, date
import base64
import redis
redis_host = os.getenv('REDIS_HOST', 'redis')  # Default to 'redis' if not set
redis_port = int(os.getenv('REDIS_PORT', 6379))

r = redis.Redis(host=redis_host, port=redis_port, db=0)



app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # Secret key for sessions
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:@db/servesmart"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

# Initialize database
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
    qr_id = db.Column(db.String(36), nullable=False, unique=True)  # UUID as a unique identifier
    entry = db.Column(db.String(20), nullable=True)


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
    return render_template('admindashboard.html')

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
    from tasks import generate_qr_task  # ✅ Lazy import here
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



    # Start Celery task for QR generation
    if meal and username:
        meal_date_str = meal_date_obj.strftime("%Y-%m-%d")  # Convert date to string
        print(f"Sending task with: {username}, {meal}, {meal_date_obj}")
        generate_qr_task(username, meal, meal_date_str)
        flash("Your QR is being generated in the background. Please check back later.", "success")
        qr_generated = True
        session['qr_generated'] = qr_generated
        session['meal'] = meal

    session.pop('qr_generated', None)



    current_date = datetime.today().date()
    date_options = [
        current_date,
        current_date + timedelta(days=1),
        current_date + timedelta(days=2)
    ]

    return render_template('commondininghall.html', qr_generated=qr_generated, meal=meal, current_date=current_time.date(), date_options=date_options)

@app.route('/generated_qrs')
def generated_qrs():
    if 'username' not in session:
        return redirect(url_for('index'))

    # Fetch all generated QR codes for the logged-in user from the database
    username = session['username']
    qr_codes = Meals.query.filter_by(username=username).all()

    return render_template('generated_qrs.html', qr_codes=qr_codes)

@app.route('/scan_qr')
def scan_qr():
    # Check if the user is logged in
    if 'username' not in session:
        return redirect(url_for('index'))  # Redirect to login page if not logged in
    # If logged in, render the QR scanner page
    return render_template('scan_qr.html')  # Replace with your actual template name

# Route for operators
@app.route('/operators')
def operators():
    # Check if the user is logged in
    if 'username' not in session:
        return redirect(url_for('index'))  # Redirect to login page if not logged in
    # If logged in, render the operators page
    return render_template('operators.html')  # Replace with your actual template name

# Route for meal details
@app.route('/meal_details')
def meal_details():
    # Check if the user is logged in
    if 'username' not in session:
        return redirect(url_for('index'))  # Redirect to login page if not logged in
    # If logged in, render the meal details page
    return render_template('meal_details.html')


@app.route('/validate_qr', methods=['POST'])
def validate_qr():
    data = request.get_json()
    qr_uuid = data.get('qr_uuid')

    # Validate UUID format
    try:
        uuid_obj = uuid.UUID(qr_uuid, version=4)  # Checks if it is a valid UUID v4
    except ValueError:
        return jsonify({"message": "Invalid QR code format."})

    # Search for the UUID in the database
    meal = Meals.query.filter_by(qr_id=str(uuid_obj)).first()
    if meal:
        if meal.entry == "filled":
            return jsonify({"message": "This QR code has already been validated."}), 200
        else:
            # If a meal is found, mark it as "filled"
            meal.entry = "filled"
            db.session.commit()
            return jsonify({"message": f"QR code validated for meal: {meal.meal_type} on {meal.date}"}), 200
    else:

        return jsonify({"message": "Invalid or unregistered QR code."}), 404
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)

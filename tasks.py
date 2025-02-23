from celery import Celery
from flask import Flask

def make_celery():
    app = Flask(__name__)  # Create a new Flask app instance
    app.config.update(
        broker_url='redis://redis:6379/0',
        result_backend='redis://redis:6379/0'
    )

    celery = Celery(
        app.import_name,
        broker=app.config['broker_url'],
        backend=app.config['result_backend']
    )
    celery.conf.update(app.config)

    return celery

celery = make_celery()

@celery.task
def generate_qr_task(username, meal, meal_date_str):
    print(f"Received in task: {username}, {meal}, {meal_date_str}")  # Debugging
    from flask import current_app  # Import inside function to avoid circular imports
    from io import BytesIO
    import uuid
    import segno
    from main import db, Meals, app

    with app.app_context():
        unique_id = str(uuid.uuid4())
        qr = segno.make(unique_id)
        img_buffer = BytesIO()
        qr.save(img_buffer, kind='png', scale=10)
        img_binary = img_buffer.getvalue()

        new_meal = Meals(username=username, qrcode=img_binary, qr_id=unique_id, meal_type=meal, date=meal_date_str)
        db.session.add(new_meal)
        db.session.commit()

        return "QR code generated"
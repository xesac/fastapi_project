from app.task.celery_app import celery
from PIL import Image
from pathlib import Path
from pydantic import EmailStr
import smtplib
from app.config.config import settings
from fastapi import BackgroundTasks 
from app.task.email_templates import create_booking_confirmation_template

@celery.task
def process_pic(path: str):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized = im.resize((1000, 500))
    im_resized2 = im.resize((200, 100))
    im_resized.save(f'app/static/images/resized_1000_500{im_path.name}')
    im_resized2.save(f'app/static/images/resized_1000_500{im_path.name}')

@celery.task
def send_booking_confirmation_email(
    booking: dict,
    email_to: EmailStr

):
    msg_content = create_booking_confirmation_template(booking, email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)

        server.send_message(msg_content)
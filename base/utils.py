import os
# import threading
# from django.core.mail import send_mail
# from django.conf import settings
from django.utils import timezone

def get_file_path(instance, filename):
    # Get the current timestamp
    timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    # Get the file extension
    extension = os.path.splitext(filename)[1]
    # Generate a new filename with the timestamp
    new_filename = f"eventsradar-{timestamp}{extension}"
    return os.path.join("uploads", new_filename)

# def sendmail(mail, subject, message):
#     threading.Thread(target=send_email, args=(message, mail,subject )).start()


# base/utils.py
import threading
from django.core.mail import send_mail
from django.conf import settings

def send_email(message, recipient_email, subject):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient_email],
        fail_silently=False,
    )

def sendmail(message, recipient_email, subject):
    threading.Thread(target=send_email, args=(message, recipient_email, subject)).start()
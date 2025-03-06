import smtplib
import ssl
import threading
from datetime import datetime, timezone, timedelta

from django.db import models

from authentication.models import User
from config.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

THEMES = ["Marine Biodiversity and Conservation",
          "Sustainable Fisheries, Aquaculture and Blue Economy",
          "Marine Biotechnology and Genomics",
          "Marine Natural Products and Drug Discovery",
          "Polar Biology, Climate Change and Ocean Health",
          "Marine Microbiology and Anti-Microbial Resistance"
          ]

def send_email(message, receiver, subject="ICMBGSD 25  Registration/Login verification"):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = EMAIL_HOST_USER
    receiver_email = receiver
    password = EMAIL_HOST_PASSWORD
    text = message
    message = f'Subject: {subject}\n\n{text}'

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        # utf-8 encoding is used to support special characters
        message = message.encode('utf-8')
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


class Speaker(models.Model):
    name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='speakers', null=True, blank=True)
    facebook = models.URLField(max_length=100, null=True, blank=True)
    twitter = models.URLField(max_length=100, null=True, blank=True)
    google_scholar = models.URLField(max_length=100, null=True, blank=True)
    linkedin = models.URLField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Faq(models.Model):
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)

    def __str__(self):
        return self.question


class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='sponsors', null=True, blank=True)
    website = models.URLField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    date = models.DateField()
    time = models.TimeField()
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    day = models.CharField(max_length=100, choices=(('Day 1', 'Day 1'), ('Day 2', 'Day 2'), ('Day 3', 'Day 3')))

    class Meta:
        ordering = ['date', 'time']
        verbose_name_plural = 'Schedule'

    def __str__(self):
        return self.title


class Committee(models.Model):
    SIZE_CHOICES = [
        (1, 'Small'),
        (2, 'Medium'),
        (3, 'Large'),
    ]

    name = models.CharField(max_length=100)
    size_on_website = models.IntegerField(choices=SIZE_CHOICES)
    slug = models.SlugField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['size_on_website']

    def __str__(self):
        return self.name


class CommitteeMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='committee', null=True, blank=True)
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)
    facebook = models.URLField(max_length=100, null=True, blank=True)
    twitter = models.URLField(max_length=100, null=True, blank=True)
    google_scholar = models.URLField(max_length=100, null=True, blank=True)
    linkedin = models.URLField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Gallery(models.Model):
    caption = models.CharField(max_length=100)

    def __str__(self):
        return self.caption

class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(default='gallery/')

class Theme(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name


def generate_otp():
    import random
    while True:
        otp = ''.join([str(random.randint(0, 9)) for i in range(6)])
        if not OTP.objects.filter(otp=otp).exists():
            return otp


class OTP(models.Model):
    otp = models.CharField(max_length=6, default=generate_otp, unique=True)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.otp

    @property
    def expired(self):
        # Assuming self.created_at is an offset-aware datetime object
        created_at_with_tz = self.created_at.replace(tzinfo=timezone.utc)

        # Use datetime.now(timezone.utc) to get an offset-aware current datetime
        current_datetime = datetime.now(timezone.utc)

        # Perform the subtraction with both datetime objects being offset-aware
        return current_datetime - created_at_with_tz > timedelta(minutes=5)

    def is_valid(self):
        return not self.expired and not self.used

    def send_email(self):
        msg = "Your OTP for login to ICMBGSD 25  is  " + self.otp + "  Please enter this OTP to login."
        threading.Thread(target=send_email, args=(msg, self.user.email, self.otp)).start()


class PaperAbstract(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=500)
    authors = models.CharField(max_length=500)
    abstract = models.TextField(blank=True, null=True)
    keywords = models.CharField(max_length=500)
    file = models.FileField(upload_to='abstracts', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    theme = models.CharField(max_length=100, choices=[(i, i) for i in THEMES], default=THEMES[0])
    presentation = models.CharField(max_length=100, choices=(("oral", 'oral'), ('poster', 'poster')),default='oral')

    def __str__(self):
        return self.title

    def send_email(self):
        msg = (f"New Abstract {self.title}, Submitted  by {self.user.full_name} ({self.user.email})"
               f" on the theme {self.theme} use the link to download the file https://icmbgsd2025.cusat.ac.in{self.file.url}")
        threading.Thread(target=send_email, args=(msg, EMAIL_HOST_USER, "New abstract submission")).start()



class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class TravelGrant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="travel_grants")
    cv = models.FileField(upload_to='cvs/')
    bank_name = models.CharField(max_length=50)
    ifsc = models.CharField(max_length=50)
    acc_number = models.CharField(max_length=50)
    institiution = models.CharField(max_length=50, blank=False, null=False, default="College/Institiution")

    def __str__(self):
        return self.user.get_full_name()

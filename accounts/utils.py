from django.core.mail import EmailMessage
import random
from django.conf import settings
from .models import User, OneTimePassword
from django.contrib.sites.shortcuts import get_current_site



def send_generated_otp_to_email(email, request): 
    subject = "One-Time Passcode for Email Verification"
    otp = random.randint(100000, 999999)  # Correct the range
    current_site = get_current_site(request).domain
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Handle the case where no user is found
        return "User not found."

    email_body = f"Hi {user.first_name}, thanks for signing up on {current_site}. Please verify your email with this one-time passcode: {otp}"
    from_email = settings.EMAIL_HOST_USER  # Make sure this is set in your settings
    otp_obj = OneTimePassword.objects.create(user=user, otp=otp)

    # Send the email 
    d_email = EmailMessage(subject=subject, body=email_body, from_email=from_email, to=[email])
    d_email.send()
    return "OTP sent successfully."


def send_normal_email(data):
    email=EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']]
    )
    email.send()

from django.core.mail import EmailMessage
from django.conf import settings

def send_course_assignment_email(email, course_title, request=None):
    subject = 'You have been assigned to a new course!'
    current_site = get_current_site(request).domain if request else 'our platform'
    email_body = (f"Dear User,\n\n"
                  f"You have been assigned to the course '{course_title}' on wwww.bwenge.com. "
                  f"Please log in to your account to view the details.\n\n"
                  f"Best regards,\nYour Platform Team")
    
    from_email = settings.DEFAULT_FROM_EMAIL
    
    try:
        email_message = EmailMessage(subject=subject, body=email_body, from_email=from_email, to=[email])
        email_message.send()
        print(f"Email successfully sent to {email}")
    except Exception as e:
        print(f"Failed to send email to {email}: {e}")

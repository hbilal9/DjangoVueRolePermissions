from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def sendMail(to, template,  subject, content, file = None):
    html_content = render_to_string(template, content)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [to])
    email.attach_alternative(html_content, "text/html")
    if file:
        email.attach_file(file)
    email.send()
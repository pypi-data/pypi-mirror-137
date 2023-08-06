from django.shortcuts import render
from django.core.mail import EmailMessage
from django.conf import settings
import threading
from threading import Thread

# Create your views here.

class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list, replyto):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.reply_to = replyto
        threading.Thread.__init__(self)

    def run (self):
        msg = EmailMessage(self.subject, self.html_content, settings.EMAIL_HOST_USER, self.recipient_list, reply_to=self.reply_to)
        msg.content_subtype = "html"
        msg.send(fail_silently=False)

def send_html_mail(subject, html_content, recipient_list, replyto):
    EmailThread(subject, html_content, recipient_list, replyto).start()

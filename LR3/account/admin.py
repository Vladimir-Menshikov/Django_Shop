from django.contrib import admin
from .models import Profile
from django.core.mail import send_mail
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string
from .views import send_mail_multiproc
from jinja2 import Template
from multiprocessing import Process, Queue, Manager
import logging
from LR3.settings import EMAIL_HOST_USER
from threading import Thread
from static_vars import static_vars
from django.db.models import QuerySet

logger = logging.getLogger(__name__)

def process_sent_queue(queue):
    while True:
        if not queue.empty():
            address, message = queue.get()
            send_mail('Activate your account', message, EMAIL_HOST_USER, [address], False)


@static_vars(IS_ACTIVE=False)
def send_email_multiproc(address, message):
    if not send_email_multiproc.IS_ACTIVE:
        send_email_multiproc.queue = Manager().Queue()
        process = Process(target=process_sent_queue, args=(send_email_multiproc.queue,))
        process.daemon = True
        process.start()
        send_email_multiproc.IS_ACTIVE = True
    send_email_multiproc.queue.put((address, message))



class ProfileAdmin(admin.ModelAdmin):

    def send_message(self, request, queryset, form=None, change=None):     
        html = open('account/templates/account/acc_active_email.html').read()
        template = Template(html)
        current_site = get_current_site(request)  
       
        for q in queryset:
            message = template.render(user = q.user, 
                                      domain = current_site.domain,
                                      uid = urlsafe_base64_encode(force_bytes(q.user.id)),
                                      token = account_activation_token.make_token(q.user),)  
            send_mail_multiproc([q.user.email], message)
            #send_mail('Activate your account', message, EMAIL_HOST_USER, [q.user.email])
            logger.info("Verification message sent to user " + q.user.username)

            
    send_message.short_description = "Send verification mail"
    list_display = ['user', 'date_of_birth', 'photo', 'verified']
    actions = [send_message]

admin.site.register(Profile, ProfileAdmin)
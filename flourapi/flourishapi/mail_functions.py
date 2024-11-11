import threading
import traceback
from flourishapi.models import *
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from flourishapi.utils import *

frontend_url = settings.FRONTEND_URL

class Emailthread(threading.Thread):

    def __init__(self,type_id,email_settings, **kwargs):
        self.type_id = type_id
        self.email_settings = email_settings
        self.kwargs = kwargs
        threading.Thread.__init__(self)
        
    def run(self):
        kwargs = self.kwargs
        try:
            mail_function = send_email(self.type_id,self.email_settings, **kwargs)
            if mail_function == True:
                return True
            else:
                return False
        except Exception as e:
            print('threading function exception',e)
            return e 
        

def email_host_assign(email_settings=None):
    """
        this function initialize SMTP Host user,port,tls and password
        
    """
    # Get Email credentials From Admin Settings ::

    # email = EmailSettings.objects.get(emailsettingstypeid=email_settings)
    # settings.EMAIL_HOST = email.host
    # settings.EMAIL_HOST_USER = email.email
    # settings.EMAIL_HOST_PASSWORD = email.password
    # settings.EMAIL_PORT = email.port
    # settings.EMAIL_USE_TLS = True

    settings.EMAIL_HOST = 'smtp.gmail.com'
    settings.EMAIL_HOST_USER = 'selvakumar05352@gmail.com'
    settings.EMAIL_HOST_PASSWORD = 'rxai efhm gdnj lhwz'
    settings.EMAIL_PORT = '587'
    settings.EMAIL_USE_TLS = True
    return settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD,settings.EMAIL_HOST,settings.EMAIL_PORT,settings.EMAIL_USE_TLS


def send_email(emailtype=None,email_settings=None,**kwargs):

    try:
        # Call Functions For Admin Email credentials
        email_host_assign(email_settings)
        from_address = settings.EMAIL_HOST_USER
      
        # Template =   getObject(EmailTemplate,{'emailtypeid':emailtype})
        # email_subject = Template.email_subject
        # email_content = Template.email_content

        email_subject = 'Here’s your password reset link'
        email_content = 'hi yours password is verifications'
        bcc = None

        if emailtype == VelanEmailType.PASSWORD_RESET_LINK:
            to_address = kwargs['to_address']
            reset_link = kwargs.get('absurl')
            html_content = render_to_string('reset-password.html', {'reset_link': reset_link})
            subject = email_subject
        else:
            pass
        text = strip_tags(html_content) 
        email_msg = EmailMultiAlternatives(subject, text, from_address, [to_address])
        email_msg.attach_alternative(html_content, 'text/html')
        email_msg.send()
        return True

    except Exception as e:
        print('send email function exception exception exception', str(e),)
        print('send email function traceback traceback', traceback.format_exc())
        return False
    
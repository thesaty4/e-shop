from django.core.mail import EmailMultiAlternatives
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.conf import settings
# Sending Email
import platform
import socket
def login_detect(context_dict={}):
    mail_subject = 'Recent Login at E-SHOP'
    my_system = platform.uname()

    a=(f"System: {my_system.system}")
    b=(f"Node Name: {my_system.node}")
    c=(f"Release: {my_system.release}")
    d=(f"Version: {my_system.version}")
    e=(f"Machine: {my_system.machine}")
    f=(f"Processor: {my_system.processor}")
    host="Host Name : "+str(socket.gethostname())
    ip="IP Address : "+str(socket.gethostbyname(socket.gethostname()))
    # print(context_dict['checkout'][0])
    message  = a+"<br>"+b+"<br>"+c+"<br>"+d+"<br>"+e+"<br>"+f+"<br>"+host+"<br>"+ip
    # to_email = context_dict['user'].email
    print(context_dict['user'])
    to_email = context_dict['user']
    # for including css(only inline css works) in mail and remove autoescape off
    email = EmailMultiAlternatives(mail_subject,
        "Order Summery",      # necessary to pass some message here
        settings.EMAIL_HOST_USER,
        [to_email]
    )
    try:
        email.attach_alternative(message, "text/html")
        email.send(fail_silently=False)
    except: a=0
def order_action(context_dict={}):
    mail_subject = 'Recent Order Status'
    # print(context_dict['checkout'][0])
    if(context_dict['action']=='cancel'):   
        message  = "Your Order : <b>"+str(context_dict['checkout'][0])+"<b><br>has been cancelled.<br> .<br>Thank you. <br>E-SHOP Team"
    else:
        message  = "Your Order : <b>"+str(context_dict['checkout'][0])+"<b><br> has been shipped.<br> Your order shipped after 5 or 6 day of order.<br>Thank you for trusting with us, <br>E-SHOP Team"
    # to_email = context_dict['user'].email
    to_email = context_dict['email']
    # for including css(only inline css works) in mail and remove autoescape off
    email = EmailMultiAlternatives(mail_subject,
        "Order Summery",      # necessary to pass some message here
        settings.EMAIL_HOST_USER,
        [to_email]
    )
    try:
        email.attach_alternative(message, "text/html")
        email.send(fail_silently=False)
    except: a=0

def cancel_order(context_dict={}):
    mail_subject = 'Cancellation Order Details'
    message  = "Your Order : <b>"+context_dict['checkout']+"<b><br> are under cancellation.<br>Thank you, <br>E-SHOP Team"
    # to_email = 'satyamishra559@gmail.com'
    to_email = context_dict['user'].email
    # for including css(only inline css works) in mail and remove autoescape off
    email = EmailMultiAlternatives(mail_subject,
        "Order Summery",      # necessary to pass some message here
        settings.EMAIL_HOST_USER,
        [to_email]
    )
    try:
        email.attach_alternative(message, "text/html")
        email.send(fail_silently=False)
    except: a=0

def send_mail(template_src,context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result) #, link_callback=fetch_resources)
    pdf = result.getvalue()
    filename = 'Invoice_'+str(context_dict['checkout'])+'.pdf'
    mail_subject = 'Recent Order Details'
    template = get_template('payment/emailinvoice.html')
    message  = template.render(context_dict)
    to_email = context_dict['user'].email
    # for including css(only inline css works) in mail and remove autoescape off
    email = EmailMultiAlternatives(mail_subject,
        "Order Summery",      # necessary to pass some message here
        settings.EMAIL_HOST_USER,
        [to_email]
    )
    try:
        email.attach_alternative(message, "text/html")
        email.attach(filename, pdf, 'application/pdf')
        email.send(fail_silently=False)
    except:
        return 0
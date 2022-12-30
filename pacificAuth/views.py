from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.urls import NoReverseMatch,reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.core.mail import send_mail,EmailMultiAlternatives
from django.core.mail import BadHeaderError,send_mail
from django.core import mail
from django.conf import settings
from django.views.generic import View
from pacificBuy import settings
from .utils import TokenGenerator ,generate_token
import threading
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import PasswordResetTokenGenerator
class EmailThread(threading.Thread):
    def __init__(self,email_message):
        self.email_message=email_message
        threading.Thread.__init__(self)
    def run(self):
        self.email_message.send()    


# Create your views here.
def signup (request):
    if request.method=="POST":
        first_name = request.POST['name']
       
        email = request.POST['email']
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']
        if len(password)<8:
            messages.warning(request,"Password is too Short")
            return render(request,'pacificAuth/signup.html')

        if password !=confirm_password or len(password)<8:
            messages.warning(request,"Password is Not Matching")
            return render(request,'pacificAuth/signup.html')
        
        try:
            if User.objects.get(username=email):
                messages.warning(request,"Username is Taken")
                return render(request,'pacificAuth/signup.html')

        except Exception as identifier:
            pass   

        user = User.objects.create_user(email,email,password)
        user.is_active =False
        user.save()
        user.first_name = first_name
        current_site = get_current_site(request)
        email_subject = "Activate Your Account"
        message= render_to_string('pacificAuth/activate.html',{
            'user':user,
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
        })
        email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
        EmailThread(email_message).start()
        messages.info(request,"Activate Your Account by clicking link on your email")
        return redirect('/auth/login')
        messages.info(request,"Signup Successfully!  Please Login")
        return redirect('/auth/login')
    
    
    
    return render(request,'pacificAuth/signup.html')

def handlelogin (request):
    if request.method=="POST":
        username = request.POST['email']
        userpassword = request.POST['pass1']
        myuser = authenticate(username=username,password=userpassword)

        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Successfully")
            return redirect('/')

        else:
            messages.error(request,"Something Went Wrong")
            return redirect('/auth/login/')    
    return render(request,'pacificAuth/login.html')

def handlelogout(request):
    logout(request)
    messages.success(request,"logout successfully")
    return redirect('/auth/login')    

class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None

        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,"Account Activated Successfully")
            return redirect('/auth/login')
        return render(request,'pacificAuth/activatefail.html')    

class RequestResetPassword(View):
    def get(self,request):
        return render(request,'pacificAuth/reset-password.html')

    def post(self,request):
        email = request.POST['email']
        user = User.objects.filter(email=email)

        if user.exists():
            current_site = get_current_site(request)
            email_subject = "Reset Your Password"
            message= render_to_string('pacificAuth/reset-user-password.html',{
            
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
            'token':PasswordResetTokenGenerator().make_token(user[0])
        })
        email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
        EmailThread(email_message).start()
        messages.info(request,"WE have sent you a email to reset your password")
        return redirect('/auth/request-reset-password/')

class SetNewPassword(View):
    def get(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,"Password Reset link is Invalid")
                return render(request,'pacificAuth/reset-password.html')
        except DjangoUnicodeDecodeError as identifier:
            pass

        return render(request,'pacificAuth/set-new-password.html',context)

    
    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']
        if password !=confirm_password:
            messages.warning(request,"Password is Not Matching")
            return render(request,'pacificAuth/set-new-password.html')
        
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,"Password reset Success Please Login with New Password")
            return redirect('/auth/login/')
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request,"Something went Wrong")
            return render(request,'pacificAuth/set-new-password.html',context)

        return render(request,'pacificAuth/set-new-password.html',context)        








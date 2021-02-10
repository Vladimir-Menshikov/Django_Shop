from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm
from .models import Profile
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.models import User 
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from .tokens import account_activation_token
import logging
from LR3.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    logger.info("User " + q.user.username + " logged in")
                    return HttpResponse('Authenticated successfully')                    
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            logger.info("User " + new_user.username + " registered")
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})

def activate(request, uidb64, token):  
        try:  
            uid = force_text(urlsafe_base64_decode(uidb64))  
            user1 = User.objects.get(id=uid) 
            profile = Profile.objects.get(user=user1)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
            profile = None  
            logger.exception("User activation error")
        if profile is not None and account_activation_token.check_token(profile.user, token):  
            profile.is_active = True  
            profile.verified = True
            profile.save()  
            logger.info("User " + user1.username + " activated account")
            return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
        else:  
            return HttpResponse('Activation link is invalid!')

def send_mail_multiproc(address, message):
    send_mail('Activate your account', message, EMAIL_HOST_USER, [address], False)

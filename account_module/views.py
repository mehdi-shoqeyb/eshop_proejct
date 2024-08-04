from django.contrib.auth import login,logout
from django.http import Http404, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import View
from utils.email_service import send_email

from .forms import RegisterForm, LoginForm, ForgetPasswordForm, ResetPasswordForm
from .models import User


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register.html', context)

    def post(self,request: HttpRequest):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            user: bool = User.objects.filter(email__exact=user_email).exists()
            if user == True:
                register_form.add_error('email', 'ایمیل وارد شده قبلا در این سایت ثبت نام کرده است')
                context = {
                    'register_form': register_form
                }
                return render(request, 'account_module/register.html', context)
            else:
                new_user = User(email=user_email,
                                email_active_code=get_random_string(72),
                                is_active=False,
                                username=user_email
                                )
                new_user.set_password(user_password)
                new_user.save()
                send_email("فعال سازی حساب کاربری",new_user.email,{'user':new_user},'emails/activate_account.html')
                return redirect(reverse('login-page'))
        else:
            context = {
                'register_form': register_form
            }
            return render(request, 'account_module/register.html', context)


class ActiveAccountView(View):
    def get(self, request, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            user.is_active = True
            user.email_active_code = get_random_string(72)
            user.save()
            return redirect(reverse('login-page'))
        else:
            raise Http404


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login.html', context)

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_password = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                is_password_correct = user.check_password(user_password)
                if is_password_correct == True:
                    if user.is_active == True:
                        login(request,user)
                        return redirect(reverse('home_page'))
                    else:
                        login_form.add_error('email', 'حساب کاربری شما فعال نشده است')
                else:
                    login_form.add_error('password', 'رمز اشتباه است')
            else:
                login_form.add_error('email', 'کاربری با مشخصات وارد شده یافت نشد')

            context = {
                'login_form': login_form
            }
            return render(request, 'account_module/login.html', context)

class ForgetPasswordView(View):
    def get(self,request: HttpRequest):
        forget_Password_Form = ForgetPasswordForm()
        context = {
            'forget_Password_Form':forget_Password_Form
        }
        return render(request,'account_module/forget_password.html',context)

    def post(self, request: HttpRequest):
        forget_Password_Form = ForgetPasswordForm(request.POST)
        if forget_Password_Form.is_valid():
            user_email = forget_Password_Form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                send_email('بازیابی کلمه عبور',user.email,{'user':user},'emails/reset_password.html')
        context = {
            'forget_Password_Form': ForgetPasswordForm
        }
        return render(request, 'account_module/forget_password.html', context)

class ResetPasswordView(View):
    def get(self,request: HttpRequest,active_code):
        user : User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return Http404
        else:
            reset_password_form = ResetPasswordForm()
        context = {
            'reset_password_form' : reset_password_form,
            'user':user
        }
        return render(request,'account_module/reset_password.html',context)

    def post(self,request: HttpRequest,active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return Http404
        reset_password_form = ResetPasswordForm(request.POST)
        if reset_password_form.is_valid():
            user_new_password = reset_password_form.cleaned_data.get('password')
            user.set_password(user_new_password)
            user.email_active_code = get_random_string(72)
            user.is_active = True
            user.save()
            return redirect(reverse('login-page'))

        context = {
            'reset_password_form': reset_password_form,
            'user': user
        }

        return render(request, 'account_module/reset_password.html', context)

class LogOutView(View):
    def get(self,request):
        logout(request)
        return redirect(reverse('login-page'))
    
        

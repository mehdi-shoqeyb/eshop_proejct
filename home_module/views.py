from typing import Any
from django.db.models import Count
from django.http import HttpRequest,JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.utils import timezone
from django.shortcuts import render
import json
from chat_module.models import ChatRoom
from django.contrib.auth import login,logout

from django.views.generic.base import TemplateView,View

from product_module.models import Product , ProductCategory
from site_module.models import SiteSetting, Slider
from utils.convertors import group_list
from utils.email_service import send_email

from account_module.models import User,OTP
from account_module.forms import TmepUserEmailForm,TmepUserOTPForm
from datetime import datetime

# class HomeView(View):
#     template_name = 'home_module/index_page.html'
    
#     def get(self, request, *args, **kwargs):
#         context = {}
        
#         if not request.user.is_authenticated:
#             context.update({
#                 'temp_user_email_form': TmepUserEmailForm(),
#                 'temp_user_otp_form': TmepUserOTPForm(),
#                 'is_logged_in': False
#             })
#         else:
#             context['is_logged_in'] = True

#         sliders = Slider.objects.filter(is_active=True)
#         latest_products = Product.objects.filter(is_active=True, is_delete=False).order_by('-id')[:12]
#         most_visited_products = Product.objects.filter(is_active=True, is_delete=False).annotate(visit_count=Count('productvisit')).order_by('-visit_count')[:12]
#         categories = list(ProductCategory.objects.annotate(products_count=Count('product_categories')).filter(is_active=True, is_delete=False, products_count__gt=0)[:6])
        
#         categories_products = [
#             {
#                 'id': category.id,
#                 'title': category.title,
#                 'products': category.product_categories.all()
#             }
#             for category in categories
#         ]

#         context.update({
#             'sliders': sliders,
#             'latest_products': group_list(latest_products, 4),
#             'most_visited_products': group_list(most_visited_products, 4),
#             'categories_products': categories_products
#         })

#         return render(request, self.template_name, context)

class HomeView(TemplateView):
    template_name = 'home_module/index_page.html'
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if not self.request.user.is_authenticated :
            context['is_logged_in'] = False
        elif self.request.user.is_superuser:
            pass
        else:
            context['username'] = self.request.user.username
            context['is_logged_in'] = True
            chatroom, created = ChatRoom.objects.get_or_create(user=self.request.user)
            
            if created:
                support_users = User.objects.filter(is_superuser=True)
                chatroom.support_user.set(support_users)
                chatroom.save()
                
            context['room_id']=chatroom.room_id

        sliders = Slider.objects.filter(is_active=True)
        context['sliders'] = sliders
        latest_products = Product.objects.filter(is_active=True, is_delete=False).order_by('-id')[:12]
        most_visited_products = Product.objects.filter(is_active=True, is_delete=False).annotate(visit_count=Count('productvisit')).order_by('-visit_count')[:12]
        context['latest_products'] = group_list(latest_products, 4)
        context['most_visited_products'] = group_list(most_visited_products, 4)
        categories = list(ProductCategory.objects.annotate(products_count=Count('product_categories')).filter(is_active=True, is_delete=False, products_count__gt=0)[:6])
        categories_products = []
        for category in categories:
            item = {
                'id': category.id,
                'title': category.title,
                'products': (category.product_categories.all())
            }
            categories_products.append(item)

        context['categories_products'] = categories_products

        return context
    
def loginemail(request:HttpRequest):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if not email:
            return HttpResponse({'success': False, 'errors': 'Email not provided'}, status=400)
        
        print(email)
        
        user = User.objects.filter(email__exact=email).exists()
        
        if user == True:
            user = User.objects.get(email=email)
            OTP.generate_otp(user=user)
            otp = OTP.objects.get(user=user)
            otp_code = otp.code
            send_email('فعال سازی حساب کاربری',user.email,{'otp_code':otp_code},'emails/otp_active_account.html')
            return HttpResponse('رمز یکبار مصرف به ایمیل شما ارسال شد')
        else:
            new_user = User(email=email,
                            is_active=False,
                            username=email
                        )
            new_user.save()
            OTP.generate_otp(user=new_user)
            otp = OTP.objects.get(user=new_user)
            otp_code = otp.code
            send_email('فعال سازی حساب کاربری',new_user.email,{'otp_code':otp_code},'emails/otp_active_account.html')
            return HttpResponse({'success': True, 'errors': 'رمز یکبار مصرف به ایمیل شما ارسال شد'})
        
def otpchek(request:HttpRequest):
    if request.method == 'POST':
        otp_code = request.POST.get('otp')
        email = request.POST['email']
        print(otp_code)
        user = User.objects.filter(email__exact=email).first()
        db_otp = OTP.objects.filter(user=user).first()
        if otp_code == db_otp.code :
            if db_otp.expiry_time > timezone.now():
                user.is_active =True
                user.save()
                login(request,user)
                print('user logged in')
                return HttpResponse('ورود به حساب کاربری با موفقیت انجام شد')
            else:
                otp = OTP.objects.get(user=user)
                OTP.generate_otp(user=user)
                send_email('فعال سازی حساب کاربری',user.email,{'otp_code':otp_code},'emails/otp_active_account.html')
                return HttpResponse('وقت رمز یکبار مصرف به اتمام رسید.یک رمز جدید به ایمیل شما ارسال شد')
        else:
            return HttpResponse('رمز وارد شده اشتباه است')
        

def site_header_component(request):
    context = {

    }
    return render(request, 'shared/site_header_component.html', context)


def site_footer_component(request):

    context = {

    }
    return render(request, 'shared/site_footer_component.html', context)


class AboutView(TemplateView):
    template_name = 'home_module/about_page.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        site_setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = site_setting
        return context


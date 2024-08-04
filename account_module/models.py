from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from datetime import datetime, timedelta
from django.utils import timezone
import pyotp
from utils.email_service import send_email

class User(AbstractUser):
    avatar = models.ImageField(upload_to='images/profile',verbose_name= "تصویر آواتار",null=True,blank=True)
    email_active_code =models.CharField(max_length=120,verbose_name='کد فعالسازی ایمیل')
    about_user = models.TextField(max_length=600,blank=True, null=True, verbose_name="درباره شخص")
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')
   
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربر'


    def __str__(self):
        # if self.first_name is not '' and self.last_name is not '':
        #     return self.get_full_name()
        return self.email
    
class OTP(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='user')
    code = models.CharField(max_length=6,verbose_name='otp code')
    expiry_time = models.DateTimeField(verbose_name='expiry time')
    
    def __str__(self):
        return self.code

    @staticmethod
    def generate_otp(user):
        try:
            user_otp = OTP.objects.get(user=user)
            if user_otp.expiry_time < timezone.now():
                otp = pyotp.TOTP(pyotp.random_base32(), interval=60)
                otp_code = otp.now()
                expiry_time = timezone.now() + timedelta(minutes=2)
                user_otp.code = otp_code
                user_otp.expiry_time = expiry_time
                user_otp.save() 
            else:
                pass
        except OTP.DoesNotExist:
            otp = pyotp.TOTP(pyotp.random_base32(), interval=60)
            otp_code = otp.now()
            expiry_time = timezone.now() + timedelta(minutes=2)
            user_otp = OTP.objects.create(code=otp_code, expiry_time=expiry_time, user=user)
            user_otp.save()
            
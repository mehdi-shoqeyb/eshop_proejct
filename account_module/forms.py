from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label="ایمیل",
        widget=forms.EmailInput(),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ]
    )
    password = forms.CharField(
        label="کلمه عبور",
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_password = forms.CharField(
        label="تکرار کلمه عبور",
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        else:
            raise ValidationError('تکرار کلمه عبور با کلمه عبور مغایرت دارد')


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="ایمیل",
        widget=forms.EmailInput(),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ]
    )
    password = forms.CharField(
        label="کلمه عبور",
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(
        label="ایمیل",
        widget=forms.EmailInput(),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ]
    )


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label="کلمه عبور",
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_password = forms.CharField(
        label="تکرار کلمه عبور",
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        else:
            raise ValidationError('تکرار کلمه عبور با کلمه عبور مغایرت دارد')

class TmepUserEmailForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'class':"contact__us-conversation-input",
            'placeholder':"اینجا بنویسید ...",
            'id':'login-input'
        }     
            ),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ]
        
    )
    
class TmepUserOTPForm(forms.Form):    
    otp_1 = forms.CharField(
        label="رمز یکبار مصرف",
        widget=forms.PasswordInput(),
        required=False,
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    
    otp_2 = forms.CharField(
        label="رمز یکبار مصرف",
        widget=forms.PasswordInput(),
        required=False,
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    otp_3 = forms.CharField(
        label="رمز یکبار مصرف",
        widget=forms.PasswordInput(),
        required=False,
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    otp_4 = forms.CharField(
        label="رمز یکبار مصرف",
        widget=forms.PasswordInput(),
        required=False,
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    
    otp_5 = forms.CharField(
        label="رمز یکبار مصرف",
        widget=forms.PasswordInput(),
        required=False,
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    
    otp_6 = forms.CharField(
        label="رمز یکبار مصرف",
        widget=forms.PasswordInput(),
        required=False,
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.data.get('email'):
            self.fields['otp_1'].required = True
            self.fields['otp_2'].required = True
            self.fields['otp_3'].required = True
            self.fields['otp_4'].required = True
            self.fields['otp_5'].required = True
            self.fields['otp_6'].required = True
        
            
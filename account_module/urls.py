from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name='register-page'),
    path('login/', views.LoginView.as_view(), name='login-page'),
    path('logout/',views.LogOutView.as_view(),name='log-out-page'),
    path('forget-password/',views.ForgetPasswordView.as_view(),name='forget-password-page'),
    path('reset-password/<active_code>', views.ResetPasswordView.as_view(), name='reset-password-page'),
    path('activate-account/<str:email_active_code>', views.ActiveAccountView.as_view(), name='activate_account-page')
]
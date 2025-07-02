from django.urls import path
from .views import SendOTP, VerifyOTP, UserProfileView 

urlpatterns = [
    path('send-otp/', SendOTP.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOTP.as_view(), name='verify_otp'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]

from rest_framework import serializers
from .models import CustomUser, OTP
from django.contrib.auth import get_user_model

User = get_user_model()

class SendOTPSerializer(serializers.Serializer):
    mobile = serializers.CharField()

class VerifyOTPSerializer(serializers.Serializer):
    mobile = serializers.CharField()
    code = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'mobile', 'referral_code', "referral_points", "is_superuser"]



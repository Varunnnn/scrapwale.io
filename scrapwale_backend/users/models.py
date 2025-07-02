from django.contrib.auth.models import AbstractUser
from django.db import models
import random
from django.utils import timezone
from datetime import timedelta

class CustomUser(AbstractUser):
    mobile = models.CharField(max_length=15, unique=True)
    referral_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    referred_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    referral_points = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self.username[:4] + str(self.pk or '')
        super().save(*args, **kwargs)

    REQUIRED_FIELDS = ['email', 'mobile']


class ReferralHistory(models.Model):
    referrer = models.ForeignKey(CustomUser, related_name="referrals_made", on_delete=models.CASCADE)
    referred = models.ForeignKey(CustomUser, related_name="referrals_received", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class OTP(models.Model):
    mobile = models.CharField(max_length=15)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)
    
    @staticmethod
    def generate_otp():
        return "123456"  # static OTP for development
    
    #def generate_otp():
        #return str(random.randint(100000, 999999))

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import OTP, CustomUser
from .serializers import SendOTPSerializer, VerifyOTPSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, ReferralHistory


User = get_user_model()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class SendOTP(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            mobile = serializer.validated_data['mobile']
            code = OTP.generate_otp()
            OTP.objects.create(mobile=mobile, code=code)
            # In production, send SMS here
            print(f"OTP for {mobile}: {code}")  # For development
            return Response({"detail": "OTP sent"}, status=200)
        return Response(serializer.errors, status=400)
    
    
class VerifyOTP(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            mobile = serializer.validated_data['mobile']
            code = serializer.validated_data['code']
            referral_code = request.data.get('referral_code')  # Get referral code if sent

            try:
                otp_obj = OTP.objects.filter(mobile=mobile, code=code).latest('created_at')
                if otp_obj.is_expired():
                    return Response({'detail': 'OTP expired'}, status=400)

                # Check if user already exists or not
                user, created = CustomUser.objects.get_or_create(username=mobile, mobile=mobile)

                # Apply referral code only for new users
                if created and referral_code:
                    try:
                        referrer = CustomUser.objects.get(referral_code=referral_code)
                        # Set referred_by relationship
                        user.referred_by = referrer
                        # Reward both users
                        user.referral_points += 20
                        referrer.referral_points += 20
                        # Save both
                        user.save()
                        referrer.save()
                        
                        # Track in referral history
                        ReferralHistory.objects.create(referrer=referrer, referred=user)
                        
                    except CustomUser.DoesNotExist:
                        pass


                tokens = get_tokens_for_user(user)
                return Response({'tokens': tokens, 'user': UserSerializer(user).data})
            
            except OTP.DoesNotExist:
                return Response({'detail': 'Invalid OTP'}, status=400)

        return Response(serializer.errors, status=400)



class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

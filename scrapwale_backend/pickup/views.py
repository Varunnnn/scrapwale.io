from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PickupRequest
from .serializers import PickupRequestSerializer

class CreatePickupView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PickupRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class ListPickupView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        pickups = PickupRequest.objects.filter(user=request.user).order_by('-created_at')
        serializer = PickupRequestSerializer(pickups, many=True)
        return Response(serializer.data)
    
    

from rest_framework.generics import ListAPIView
from .models import PickupRequest
from .serializers import PickupRequestSerializer
from users.permissions import IsAdminUserJWT

class AdminPickupListView(ListAPIView):
    queryset = PickupRequest.objects.all().order_by('-created_at')
    serializer_class = PickupRequestSerializer
    permission_classes = [IsAdminUserJWT]

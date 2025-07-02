from django.urls import path
from .views import CreatePickupView, ListPickupView


urlpatterns = [
    path('create/', CreatePickupView.as_view(), name='create-pickup'),
    path('my/', ListPickupView.as_view(), name='my-pickups'),
]

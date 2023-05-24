from django.urls import path
from .views import PostAPIView

urlpatterns = [
    path('posts', PostAPIView.as_view()),
    path('posts/<int:pk>', PostAPIView.as_view()),
]


from django.urls import path

from .views import CommentsAPIView, PostCommentAPIView

urlpatterns = [
    path('posts/<int:pk>/comments', PostCommentAPIView.as_view()),
    path('comments', CommentsAPIView.as_view())
]

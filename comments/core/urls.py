from django.urls import path

from .views import CommentsAPIView, PostCommentAPIView, CommentDeleteView

urlpatterns = [
    path('posts/<int:pk>/comments', PostCommentAPIView.as_view()),
    path('comments', CommentsAPIView.as_view()),
    path('posts/<int:post_id>/delete-comments', CommentDeleteView.as_view(), name='delete_comments'),

]

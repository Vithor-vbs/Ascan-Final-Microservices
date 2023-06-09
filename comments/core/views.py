from rest_framework.views import APIView

from rest_framework.response import Response
from .serializers import CommentSerializer
from .producer import publish

from .models import Comment

class PostCommentAPIView(APIView):
    def get(self, _, pk=None):
        comments = Comment.objects.filter(post_id=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class CommentsAPIView(APIView):
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('comment_created', serializer.data)
        return Response(serializer.data)
        
class CommentDeleteView(APIView):
    def delete(self, request, post_id):
        comments = Comment.objects.filter(post_id=post_id)
        comments.delete()
        publish('comment_deleted', post_id)
        return Response(status=204)
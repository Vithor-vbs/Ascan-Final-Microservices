from rest_framework.views import APIView 
from .serializers import PostSerializer
from .models import Post
from rest_framework.response import Response
from rest_framework import status
import requests


class PostAPIView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        # return Response([self.formatPost(p) for p in posts])
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def formatPost(self, post):
        comment = requests.get("http://127.0.0.1:8001/api/posts/%d/comments" %post.id).json()
        return {
            "id": post.id,
            "title": post.title,
            "description": post.description,
            "comments": comment

        }
    
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def put(self, request, pk):
            post = self.get_object(pk)
            serializer = PostSerializer(post, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
        
    def delete(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            post.delete()
            return Response({'message': 'Post deleted successfully.'})
        except Post.DoesNotExist:
            return Response({'message': 'Post not found.'})
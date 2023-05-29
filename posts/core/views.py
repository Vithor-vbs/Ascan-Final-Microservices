from rest_framework.views import APIView 
from .serializers import PostSerializer
from .models import Post
from rest_framework.response import Response
from .producer import publish


class PostAPIView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('post_created', serializer.data)
        return Response(serializer.data)
    
    def put(self, request, pk):
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            publish('post_updated', serializer.data)
            return Response(serializer.data)
        
    def delete(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            post.delete()
            publish('post_deleted', pk)
            return Response({'message': 'Post deleted successfully.'})
        except Post.DoesNotExist:
            return Response({'message': 'Post not found.'})
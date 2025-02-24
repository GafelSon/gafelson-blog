from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UpdateVersion, Post
from .serializers import UpdateVersionSerializer, PostCreateSerializer
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import logging
import os
from dotenv import load_dotenv

load_dotenv()  # Add this line at the top after imports

logger = logging.getLogger(__name__)

@api_view(['GET'])
def get_update_history(request):
    try:
        versions = UpdateVersion.objects.all()
        serializer = UpdateVersionSerializer(versions, many=True)
        return Response(serializer.data)
    except UpdateVersion.DoesNotExist as e:
        logger.error(f"UpdateVersion objects not found: {str(e)}")
        return Response(
            {"error": "No update versions found"},
            status=404
        )
    except Exception as e:
        logger.error(f"Error in get_update_history: {str(e)}", exc_info=True)
        return Response(
            {"error": "An unexpected error occurred"},
            status=500
        )

@csrf_exempt
@api_view(['POST'])
def create_random_posts(request):
    try:
        token = request.headers.get('X-API-Token', os.getenv('API_TOKEN'))
        if token != os.getenv('API_TOKEN'):
            return Response({"error": "Invalid token"}, status=403)
            
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            duplicate_count = serializer.validated_data.pop('duplicate_count', 1)
            target_date = serializer.validated_data.pop('target_date')

            created_posts = []
            for _ in range(duplicate_count):
                post_data = dict(serializer.validated_data)
                post_data['published'] = timezone.make_aware(
                    timezone.datetime.combine(target_date, timezone.datetime.min.time())
                )
                post = Post.objects.create(**post_data)
                created_posts.append(post)
            
            return Response({
                "message": f"Successfully created {duplicate_count} posts",
                "post_ids": [post.id for post in created_posts]
            }, status=201)
        return Response(serializer.errors, status=400)
    except Exception as e:
        logger.error(f"Error in create_random_posts: {str(e)}", exc_info=True)
        return Response({"error": str(e)}, status=500)
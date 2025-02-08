from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UpdateVersion
from .serializers import UpdateVersionSerializer
import logging

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
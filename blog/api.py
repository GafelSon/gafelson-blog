from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UpdateVersion
from .serializers import UpdateVersionSerializer

@api_view(['GET'])
def get_update_history(request):
    versions = UpdateVersion.objects.all()
    serializer = UpdateVersionSerializer(versions, many=True)
    return Response(serializer.data)
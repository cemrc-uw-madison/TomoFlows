from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def Ping(request):
    return Response({'message':'API is up and running!'})

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import CustomUserInfoSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from board.models import Board
from board.serializers import UserPostSerializer


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def info(request):
    user = request.user
    serializer = CustomUserInfoSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def postlist(request):
    user = request.user
    boards = Board.objects.filter(user = user)
    serializer = UserPostSerializer(boards, many = True)
    return Response(serializer.data, status = status.HTTP_200_OK)
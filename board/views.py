from django.shortcuts import render
from .models import Board, Comment
from .serializers import BoardSerializer, CommentSerializer, BoardDetailSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .permissions import IsOwnerOrReadOnly

# Create your views here.

class BoardList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        boards = Board.objects.all()
        serializer = BoardSerializer(boards, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request):
        serializer = BoardDetailSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user = request.user)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class BoardDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    def get_object(self, pk):
        board = get_object_or_404(Board, pk=pk)
        return board
    
    def get(self, request, pk):
        board = self.get_object(pk)
        serializer = BoardDetailSerializer(board)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        board = self.get_object(pk)
        self.check_object_permissions(request, board)
        serializer = BoardDetailSerializer(board, data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        board = self.get_object(pk)
        self.check_object_permissions(request, board)
        board.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    
class CommentPost(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    def post(self, request, pk):
        try: 
            board = Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(board = board, user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    def get(self, request, pk):
        try: 
            board = Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        comments = Comment.objects.filter(board = board)
        serializer = CommentSerializer(comments, many = True)
        return Response(serializer.data)

class CommentDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]    
    def delete(self, request, post_id, comment_id):
        board = get_object_or_404(Board, pk=post_id)
        comment = get_object_or_404(Comment, pk=comment_id, board=board)
        self.check_object_permissions(request, board)
        comment.delete()
        serializer = BoardDetailSerializer(board)
        return Response(serializer.data, status=status.HTTP_200_OK)
from todolist.models import TodoArticle
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from todolist.serializers import TodoSerializer, TodoCreateSerializer,TodoListSerializer




class TodoListView(APIView):
   
    # 조회
    def get(self, request):
        articles = TodoArticle.objects.all()
        serializer = TodoListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # 작성
    def post(self, request):
        serializer = TodoCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)        




class TodoDetailView(APIView):
    # 게시글 조회
    def get(self, request, id):
        article = get_object_or_404(TodoArticle, id=id)
        serializer = TodoSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    # 게시글 수정
    def put(self, request, id):
        article = get_object_or_404(TodoArticle, id=id)
        if request.user == article.user:
            serializer = TodoCreateSerializer(article, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)
   
   
   # 게시글 삭제
    def delete(self, request, id):
        article = get_object_or_404(TodoArticle, id=id)
        if request.user == article.user:
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)



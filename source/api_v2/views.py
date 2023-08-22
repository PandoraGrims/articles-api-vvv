from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api_v2.serializers import ArticleModelSerializer
from webapp.models import Article


@ensure_csrf_cookie
def get_csrf_token(request, *args, **kwargs):
    if request.method == "GET":
        return HttpResponse()
    return HttpResponseNotAllowed(['GET'])


class ArticleView(APIView):
    serializer_class = ArticleModelSerializer

    def get(self, request, *args, **kwargs):
        articles = Article.objects.order_by("-created_at")
        article_data = self.serializer_class(articles, many=True).data
        return Response(article_data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        article = serializer.save()
        return Response(self.serializer_class(article).data, status=status.HTTP_201_CREATED)
        # else:
        #     return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=article)
        serializer.is_valid(raise_exception=True)
        article = serializer.save()
        return Response(self.serializer_class(article).data, status=status.HTTP_200_OK)
        # else:
        #     return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailView(APIView):
    serializer_class = ArticleModelSerializer

    def get(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        article_data = self.serializer_class(article).data
        return Response(article_data)


class ArticleUpdateView(APIView):
    serializer_class = ArticleModelSerializer

    def put(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        title = request.data.get('title')
        text = request.data.get('text')

        # if title is None or text is None:
        #     return Response({"message": "Both 'title' and 'text' fields are required for update."},
        #                     status=status.HTTP_400_BAD_REQUEST)

        article.title = title
        article.text = text
        article.save()

        return Response(self.serializer_class(article).data, status=status.HTTP_200_OK)


# class ArticleUpdateView(APIView):
#     serializer_class = ArticleModelSerializer
#
#     # def put(self, request, pk, *args, **kwargs):
#     #     article = get_object_or_404(Article, pk=pk)
#
#     def put(self, request, pk, *args, **kwargs):
#         article = get_object_or_404(Article, pk=pk)
#         serializer = self.serializer_class(data=request.data, instance=article, partial=True)
#         serializer.is_valid(raise_exception=True)
#         article = serializer.save()
#         return Response(self.serializer_class(article).data, status=status.HTTP_200_OK)

# title = request.data.get('title')
# text = request.data.get('text')

# if title is None or text is None:
#     return Response({"message": " Что бы обновить статью вам нужно заполнить Заголовок и Текст "},
#                     status=status.HTTP_400_BAD_REQUEST)

# article.title = title
# article.text = text
# serializer = self.serializer_class(data=request.data, instance=article)
# serializer.is_valid(raise_exception=True)
# article = serializer.save()
# # article.save()
# return Response(self.serializer_class(article).data, status=status.HTTP_200_OK)


class ArticleDeleteView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return Response({"message": "Статья удалена"}, status=status.HTTP_204_NO_CONTENT)

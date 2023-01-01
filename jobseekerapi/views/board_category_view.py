"""View module for handling requests for boards"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from jobseekerapi.models import Category, BoardCategory, Board


class BoardCategoryView(ViewSet):
    """Board View"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single Board
        Returns:
            Response -- JSON Serialized Board"""
        try:
            category = Category.objects.get(pk=pk)
        except:
            return Response(
                {"message": "The category you requested does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BoardCategorySerializer(category)
        return Response(serializer.data)

    def list(self, request):
        filtered_board_categories = BoardCategory.objects.all()

        if "board" in request.query_params:
            board_query_value = request.query_params["board"]

            try:
                board = Board.objects.get(pk=board_query_value)
                filtered_board_categories = BoardCategory.objects.filter(board=board.id)

            except:
                return Response(
                {"message": "The board job you are searching for does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BoardCategorySerializer(filtered_board_categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        board = Board.objects.get(pk=request.data["board"])
        category = Category.objects.get(pk=request.data["category"])

        board_categories = BoardCategory.objects.filter(board=board.id)

        board_category = BoardCategory()
        board_category.board = board
        board_category.category = category

        for bc in board_categories:
            if bc.category == board_category.category:
                return Response(
                {"message": "This Category already exists on your board! Please choose another."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        board_category.save()

        serializer = BoardCategorySerializer(board_category)
        return Response(serializer.data)


    def update(self, request, pk):

        category = Category.objects.get(pk=pk)
        category.name = request.data["name"]
        category.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        board_category = BoardCategory.objects.get(pk=pk)
        board_category.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")

class BoardCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    class Meta:
        model = BoardCategory
        fields = ("id", "board", "category")

"""View module for handling requests for boards"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from jobseekerapi.models import Board, Category, Seeker


class BoardView(ViewSet):
    """Board View"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single Board
        Returns:
            Response -- JSON Serialized Board"""
        try:
            board = Board.objects.get(pk=pk)
        except:
            return Response(
                {"message": "The board you requested does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BoardSerializer(board)
        return Response(serializer.data)

    def list(self, request):
        boards = Board.objects.all()
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        seeker = Seeker.objects.get(user=request.auth.user)

        board = Board.objects.create(
            seeker=seeker,
            title=request.data["title"],
            goal=request.data["goal"],
            requirements=request.data["requirements"],
        )

        serializer = BoardSerializer(board)
        return Response(serializer.data)

    def update(self, request, pk):

        board = Board.objects.get(pk=pk)
        board.title = request.data["title"]
        board.goal = request.data["goal"]
        board.requirements = request.data["requirements"]
        board.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        board = Board.objects.get(pk=pk)
        board.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class SeekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seeker
        fields = ("id", "full_name", "username", "current_role", "elevator_pitch")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class BoardSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    seeker = SeekerSerializer(many=False)

    class Meta:
        model = Board
        fields = ("id", "seeker", "title", "goal", "requirements", "categories")

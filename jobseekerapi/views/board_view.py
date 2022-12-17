"""View module for handling requests for boards"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from jobseekerapi.models import Board, Category, Seeker, Company, Board, BoardJob, Job, BoardCategory
from datetime import date


class BoardView(ViewSet):
    """Board View"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single Board
        Returns:
            Response -- JSON Serialized Board"""

        seeker = Seeker.objects.get(user=request.auth.user)

        try:
            board = Board.objects.get(pk=pk)
        except:
            return Response(
                {"message": "The board you requested does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if seeker.id == board.seeker.id:
            serializer = BoardSerializer(board)
            return Response(serializer.data)
        else:
            return Response(
                {"message": "You don't have access to this board."},
                status=status.HTTP_403_FORBIDDEN,
            )


    def list(self, request):

        seeker = Seeker.objects.get(user=request.auth.user)

        boards = Board.objects.filter(seeker=seeker.id)

        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        seeker = Seeker.objects.get(user=request.auth.user)

        categories = request.data["categories"]
        for category in categories:
            try:
                Category.objects.get(pk=category)
            except Category.DoesNotExist:
                return Response({"message": "The category you specified does not exist"}, status = status.HTTP_404_NOT_FOUND)

        board = Board.objects.create(
            seeker=seeker,
            title=request.data["title"],
            goal=request.data["goal"],
            requirements=request.data["requirements"],
            date_started=date.today(),
            is_active=True
        )

        for category in categories:
            category_to_assign = Category.objects.get(pk=category)
            board_category = BoardCategory()
            board_category.board = board
            board_category.category = category_to_assign
            board_category.save()

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


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "name")


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ("id", "title")


class BoardJobSerializer(serializers.ModelSerializer):

    company = CompanySerializer(many=False)
    job = JobSerializer(many=False)

    class Meta:
        model = BoardJob
        fields = fields = ("id", "job", "custom_job", "company", "custom_company", "has_applied", "has_interviewed", "interview_rounds", "received_offer", "salary", "location", "salary_rating", "location_rating", "culture_rating", "leadership_rating", "team_rating", "board", "category", "interviews", "tags")

class SeekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seeker
        fields = ("id", "user", "full_name", "username", "current_role", "elevator_pitch")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class BoardSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    seeker = SeekerSerializer(many=False)
    jobs = BoardJobSerializer(many=True)

    class Meta:
        model = Board
        fields = ("id", "seeker", "title", "goal", "requirements", "date_started", "date_ended", "is_active", "categories", "jobs")

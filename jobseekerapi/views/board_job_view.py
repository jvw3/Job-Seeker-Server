"""View module for handling requests for boards"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from jobseekerapi.models import Board, BoardJob, Job, Company, Interview, Seeker, Category, Tag, BoardJobTag


class BoardJobView(ViewSet):
    """Board View"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single Board
        Returns:
            Response -- JSON Serialized Board"""
        try:
            board_job = BoardJob.objects.get(pk=pk)
        except:
            return Response(
                {"message": "The board you requested does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BoardJobSerializer(board_job)
        return Response(serializer.data)

    def list(self, request):
        filtered_board_jobs = BoardJob.objects.all()
        seeker = Seeker.objects.get(user=request.auth.user)


        # This query params will restrict users from accessing each others boards. Any request made to a board that is not theirs will result in a 403 Forbidden Status code.
        query_params_list = ["board", "category", "seeker"]
        if all(substring not in request.query_params for substring in query_params_list):
            serializer = BoardJobSerializer(filtered_board_jobs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Check if "board" is in query params on request
        elif "board" in request.query_params:
            board_query_value = request.query_params["board"]

            try:
                board = Board.objects.get(pk=board_query_value)
            except:
                return Response(
                {"message": "The board you are searching for does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check if "board" is in query params on request
        if "category" in request.query_params:
                    category_query_value = request.query_params["category"]

                    try:
                        category = Category.objects.get(pk=category_query_value)
                    except:
                        return Response(
                        {"message": "The Category you are searching for does not exist."},
                        status=status.HTTP_404_NOT_FOUND,
                    )

        # If seeker.id is equal to seeker id of the board, then we
        if seeker.id == board.seeker.id:
            if "board" and "category" in request.query_params:
                    filter_for_board = BoardJob.objects.filter(board=board.id)
                    filtered_board_jobs = filter_for_board.filter(category=category.id)
                    serializer = BoardJobSerializer(filtered_board_jobs, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            elif "board" in request.query_params:
                    filtered_board_jobs = BoardJob.objects.filter(board=board.id)
                    serializer = BoardJobSerializer(filtered_board_jobs, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                        {"message": "You do not have access to the jobs of this board."},
                        status=status.HTTP_403_FORBIDDEN,
                    )



        serializer = BoardJobSerializer(filtered_board_jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        seeker = Seeker.objects.get(user=request.auth.user)
        job = Job.objects.get(pk=request.data["job"])
        company = Company.objects.get(pk=request.data["company"])
        board = Board.objects.get(pk=request.data["board"])
        category = Category.objects.get(pk=request.data["category"])

        tags = request.data["tags"]
        for tag in tags:
            try:
                Tag.objects.get(pk=tag)
            except Category.DoesNotExist:
                return Response({"message": "The category you specified does not exist"}, status = status.HTTP_404_NOT_FOUND)

        board_job = BoardJob.objects.create(
            job=job,
            custom_job=request.data["custom_job"],
            company=company,
            custom_company=request.data["custom_company"],
            has_applied=request.data["has_applied"],
            has_interviewed=request.data["has_interviewed"],
            interview_rounds=request.data["interview_rounds"],
            received_offer=request.data["received_offer"],
            salary=request.data["salary"],
            location=request.data["location"],
            salary_rating=request.data["salary_rating"],
            location_rating=request.data["location_rating"],
            culture_rating=request.data["culture_rating"],
            leadership_rating=request.data["leadership_rating"],
            team_rating=request.data["team_rating"],
            board=board,
            category=category
        )

        for tag in tags:
            tag_to_assign = Tag.objects.get(pk=tag)
            board_job_tag = BoardJobTag()
            board_job_tag.seeker = seeker
            board_job_tag.board_job = board_job
            board_job_tag.tag = tag_to_assign
            board_job_tag.save()

        serializer = BoardJobSerializer(board_job)
        return Response(serializer.data)

    def update(self, request, pk):

        board_job = BoardJob.objects.get(pk=pk)
        job = Job.objects.get(pk=request.data["job"])
        company = Company.objects.get(pk=request.data["company"])
        board = Board.objects.get(pk=request.data["board"])
        category = Category.objects.get(pk=request.data["category"])



        board_job.job = job
        board_job.custom_job = request.data["custom_job"]
        board_job.company = company
        board_job.custom_company = request.data["custom_company"]
        board_job.has_applied = request.data["has_applied"]
        board_job.has_interviewed = request.data["has_interviewed"]
        board_job.interview_rounds = request.data["interview_rounds"]
        board_job.received_offer = request.data["received_offer"]
        board_job.received_offer = request.data["received_offer"]
        board_job.salary = request.data["salary"]
        board_job.location = request.data["location"]
        board_job.salary_rating = request.data["salary_rating"]
        board_job.location_rating = request.data["location_rating"]
        board_job.culture_rating = request.data["culture_rating"]
        board_job.leadership_rating = request.data["leadership_rating"]
        board_job.team_rating = request.data["team_rating"]
        board_job.board = board
        board_job.category = category
        board_job.save()


        return Response(None, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk):
        board_job = BoardJob.objects.get(pk=pk)
        board_job.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class BoardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = ("id", "seeker")

class InterviewSerializer(serializers.ModelSerializer):


    class Meta:
        model = Interview
        fields = ("id", "board_job", "prep", "date", "is_complete", "interview_feedback")
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "name")
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ("id", "title")


class BoardJobSerializer(serializers.ModelSerializer):

    company = CompanySerializer(many=False)
    job = JobSerializer(many=False)
    interviews = InterviewSerializer(many=True)
    tags = TagSerializer(many=True)
    board = BoardSerializer(many=False)

    class Meta:
        model = BoardJob
        fields = ("id", "job", "custom_job", "company", "custom_company", "has_applied", "has_interviewed", "interview_rounds", "received_offer", "salary", "location", "salary_rating", "location_rating", "culture_rating", "leadership_rating", "team_rating", "board", "category", "interviews", "tags", "joined")


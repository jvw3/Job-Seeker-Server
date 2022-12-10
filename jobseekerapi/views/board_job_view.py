"""View module for handling requests for boards"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from jobseekerapi.models import Board, BoardJob, Job, Company, Interview, Seeker


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
        if "board" in request.query_params:
            query_value = request.query_params["board"]

            try:
                board = Board.objects.get(pk=query_value)
            except:
                return Response(
                {"message": "The board you are searching for does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )


            if seeker.id == board.seeker.id:
                try:
                    filtered_board_jobs = BoardJob.objects.filter(board=board.id)
                except:
                    return Response(
                {"message": "You don't have access to this board."},
                status=status.HTTP_403_FORBIDDEN,
            )


        serializer = BoardJobSerializer(filtered_board_jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        job = Job.objects.get(pk=request.data["job_id"])
        company = Company.objects.get(pk=request.data["company_id"])
        board = Board.objects.get(pk=request.data["board_id"])

        board_job = BoardJob.objects.create(
            job=job,
            company=company,
            has_interviewed=request.data["has_interviewed"],
            interview_rounds=request.data["interview_rounds"],
            salary_rating=request.data["salary_rating"],
            location_rating=request.data["location_rating"],
            culture_rating=request.data["culture_rating"],
            leadership_rating=request.data["leadership_rating"],
            team_rating=request.data["team_rating"],
            board=board,
            category_state=request.data["category_state"]
        )

        serializer = BoardJobSerializer(board_job)
        return Response(serializer.data)

    def update(self, request, pk):

        board = Board.objects.get(pk=request.data["board_id"])
        job = Job.objects.get(pk=request.data["job_id"])
        company = Company.objects.get(pk=request.data["company_id"])

        board_job = BoardJob.objects.get(pk=pk)
        board_job.job = job
        board_job.company = company
        board_job.has_interviewed = request.data["has_interviewed"]
        board_job.interview_rounds = request.data["interview_rounds"]
        board_job.salary_rating = request.data["salary_rating"]
        board_job.location_rating = request.data["location_rating"]
        board_job.culture_rating = request.data["culture_rating"]
        board_job.leadership_rating = request.data["leadership_rating"]
        board_job.team_rating = request.data["team_rating"]
        board_job.board = board
        board_job.category_state = request.data["category_state"]

        board_job.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        board_job = BoardJob.objects.get(pk=pk)
        board_job.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class InterviewSerializer(serializers.ModelSerializer):


    class Meta:
        model = Interview
        fields = ("id", "board_job", "prep", "date", "is_complete", "interview_feedback")
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
    interviews = InterviewSerializer(many=True)

    class Meta:
        model = BoardJob
        fields = ("id", "job", "company", "has_interviewed", "interview_rounds", "salary_rating", "location_rating", "culture_rating", "leadership_rating", "team_rating", "board", "category_state", "interviews")

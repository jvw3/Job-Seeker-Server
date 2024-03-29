"""View module for handling requests for boards"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from jobseekerapi.models import Interview, BoardJob, InterviewPrep, Company, Job, CustomPrepInfo, Question, Seeker, Board
from datetime import datetime


class InterviewView(ViewSet):
    """Board View"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single Board
        Returns:
            Response -- JSON Serialized Board"""
        try:
            interview = Interview.objects.get(pk=pk)
        except:
            return Response(
                {"message": "The interview you requested does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = InterviewSerializer(interview)
        return Response(serializer.data)

    def list(self, request):
        filtered_interviews = Interview.objects.all()

        if "boardjob" in request.query_params:
                    query_value = request.query_params["boardjob"]

                    try:
                        board_job = BoardJob.objects.get(pk=query_value)
                        filtered_interviews = Interview.objects.filter(board_job=board_job.id)
                        serializer = InterviewSerializer(filtered_interviews, many=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    except:
                        return Response(
                        {"message": "The board job you are querying for does not exist."},
                        status=status.HTTP_404_NOT_FOUND,
                    )

        if "upcoming" in request.query_params:
            seeker = Seeker.objects.get(user=request.auth.user)
            filtered_interviews =  Interview.objects.filter(seeker=seeker.id).order_by("date")
            active_interviews = filtered_interviews.filter(is_complete=False)
            # if len(active_interviews) > 3:
            #     filtered_interviews = active_interviews[0:3]
            #     serializer = InterviewSerializer(active_interviews, many=True)
            #     return Response(serializer.data, status=status.HTTP_200_OK)
            # else:
            serializer = InterviewSerializer(active_interviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = InterviewSerializer(filtered_interviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request):

        seeker = Seeker.objects.get(user=request.auth.user)
        board_job = BoardJob.objects.get(pk=request.data["board_job"])
        interview_prep = InterviewPrep.objects.get(pk=request.data["prep"])

        interview = Interview.objects.create(
            seeker=seeker,
            board_job=board_job,
            prep=interview_prep,
            date = request.data["date"],
            is_complete = request.data["is_complete"],
            interview_team=request.data["interview_team"],
            interview_feedback = request.data["interview_feedback"],
        )

        serializer = InterviewSerializer(interview)
        return Response(serializer.data)

    def update(self, request, pk):

        board_job = BoardJob.objects.get(pk=request.data["board_job"])
        interview_prep = InterviewPrep.objects.get(pk=request.data["prep"])


        interview = Interview.objects.get(pk=pk)
        interview.board_job=board_job
        interview.prep=interview_prep
        interview.date=request.data["date"]
        interview.is_complete = request.data["is_complete"]
        interview.interview_team = request.data["interview_team"]
        interview.interview_feedback = request.data["interview_feedback"]
        interview.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        interview = Interview.objects.get(pk=pk)
        interview.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("id", "content")
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "name")

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ("id", "title")

class BoardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = ("title",)

class CustomPrepSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomPrepInfo
        fields = ("id", "title", "description", "content")

class InterviewPrepSerializer(serializers.ModelSerializer):
    custom_preps = CustomPrepSerializer(many=True)
    questions = QuestionSerializer(many=True)

    class Meta:
        model = InterviewPrep
        fields = ("id", "seeker", "company_info", "custom_preps", "questions")


class BoardJobSerializer(serializers.ModelSerializer):

    board = BoardSerializer(many=False)
    job = JobSerializer(many=False)
    company = CompanySerializer(many=False)

    class Meta:
        model = BoardJob
        fields = ("id", "job", "custom_job", "company", "custom_company", "board")


class InterviewSerializer(serializers.ModelSerializer):
    board_job = BoardJobSerializer(many=False)
    prep = InterviewPrepSerializer(many=False)
    class Meta:
        model = Interview
        fields = ("id", "board_job", "prep", "date", "is_complete", "interview_team","interview_feedback")
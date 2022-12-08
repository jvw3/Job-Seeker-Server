"""View module for handling requests for boards"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from jobseekerapi.models import Interview, BoardJob, InterviewPrep


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
        interviews = Interview.objects.all()
        serializer = InterviewSerializer(interviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        interview_prep = InterviewPrep.objects.get(pk=request.data["prep_id"])
        board_job = BoardJob.objects.get(pk=request.data["board_job_id"])

        interview = Interview.objects.create(
            board_job=board_job,
            prep=interview_prep,
            date=request.data["date"],
            is_complete = request.data["is_complete"],
            interview_feedback = request.data["interview_feedback"],
        )

        serializer = InterviewSerializer(interview)
        return Response(serializer.data)

    def update(self, request, pk):

        board_job = BoardJob.objects.get(pk=request.data["board_job_id"])
        interview_prep = InterviewPrep.objects.get(pk=request.data["prep_id"])


        interview = Interview.objects.get(pk=pk)
        interview.board_job=board_job
        interview.prep=interview_prep
        interview.date=request.data["date"]
        interview.is_complete = request.data["is_complete"]
        interview.interview_feedback = request.data["interview_feedback"]
        interview.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        interview = Interview.objects.get(pk=pk)
        interview.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class InterviewPrepSerializer(serializers.ModelSerializer):

    class Meta:
        model = InterviewPrep
        fields = ("id", "company_info", "custom_preps")

class InterviewSerializer(serializers.ModelSerializer):

    prep = InterviewPrepSerializer(many=False)
    class Meta:
        model = Interview
        fields = ("id", "board_job", "prep", "date", "is_complete", "interview_feedback")
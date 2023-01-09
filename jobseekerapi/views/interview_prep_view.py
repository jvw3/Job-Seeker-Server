"""View module for handling requests for boards"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from jobseekerapi.models import InterviewPrep, Seeker, CustomPrepInfo, Question, Interview


class InterviewPrepView(ViewSet):
    """Board View"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single Board
        Returns:
            Response -- JSON Serialized Board"""
        try:
            interview_prep = InterviewPrep.objects.get(pk=pk)
        except:
            return Response(
                {"message": "The interview prep you requested does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = InterviewPrepSerializer(interview_prep)
        return Response(serializer.data)

    def list(self, request):
        filtered_interview_preps = InterviewPrep.objects.all()

        if "currentseeker" in request.query_params:
            seeker = Seeker.objects.get(user=request.auth.user)
            filtered_interview_preps =  InterviewPrep.objects.filter(seeker=seeker.id)
        serializer = InterviewPrepSerializer(filtered_interview_preps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        seeker = Seeker.objects.get(user=request.auth.user)

        interview_prep = InterviewPrep.objects.create(
            seeker=seeker,
            company_info = request.data["company_info"]
        )

        serializer = InterviewPrepSerializer(interview_prep)
        return Response(serializer.data)

    def update(self, request, pk):

        interview_prep = InterviewPrep.objects.get(pk=pk)
        interview_prep.company_info = request.data["company_info"]
        interview_prep.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        interview_prep = InterviewPrep.objects.get(pk=pk)
        interview_prep.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("id", "content")

class CustomPrepSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomPrepInfo
        fields = ("id", "title", "description", "content")
class SeekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seeker
        fields = ("id","current_role", "elevator_pitch")

class InterviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interview
        fields = ("id", "board_job", "prep", "date", "is_complete", "interview_team","interview_feedback")

class InterviewPrepSerializer(serializers.ModelSerializer):
    seeker = SeekerSerializer(many=False)
    custom_preps = CustomPrepSerializer(many=True)
    questions = QuestionSerializer(many=True)
    class Meta:
        model = InterviewPrep
        fields = ("id", "seeker", "company_info", "custom_preps", "questions")
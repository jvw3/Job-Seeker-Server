"""View module for handling requests for boards"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from jobseekerapi.models import CustomPrepInfo, Seeker, InterviewPrep


class CustomPrepView(ViewSet):
    """Board View"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single Board
        Returns:
            Response -- JSON Serialized Board"""
        try:
            custom_prep_info = CustomPrepInfo.objects.get(pk=pk)
        except:
            return Response(
                {"message": "The custom prep info you requested does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CustomPrepSerializer(custom_prep_info)
        return Response(serializer.data)

    def list(self, request):
        custom_prep_infos = CustomPrepInfo.objects.all()
        serializer = CustomPrepSerializer(custom_prep_infos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        interview_prep = InterviewPrep.objects.get(pk=request.data["prep_id"])

        custom_prep_info = CustomPrepInfo.objects.create(
            prep=interview_prep,
            title = request.data["title"],
            description = request.data["description"],
            content = request.data["content"],
        )

        serializer = CustomPrepSerializer(custom_prep_info)
        return Response(serializer.data)

    def update(self, request, pk):

        custom_prep_info = CustomPrepInfo.objects.get(pk=pk)
        custom_prep_info.title = request.data["title"]
        custom_prep_info.description = request.data["description"]
        custom_prep_info.content = request.data["content"]

        interview_prep = InterviewPrep.objects.get(pk=request.data["prep_id"])
        custom_prep_info.prep_id = interview_prep
        custom_prep_info.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        custom_prep_info = CustomPrepInfo.objects.get(pk=pk)
        custom_prep_info.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class SeekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seeker
        fields = ("id","current_role", "elevator_pitch")

class CustomPrepSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomPrepInfo
        fields = ("id", "prep_id", "title", "description", "content")
"""View module for handling requests for boards"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from jobseekerapi.models import MeetingType


class MeetingTypeView(ViewSet):
    """Meeting Type View"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single Board
        Returns:
            Response -- JSON Serialized Board"""
        try:
            category = MeetingType.objects.get(pk=pk)
        except:
            return Response(
                {"message": "The category you requested does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def list(self, request):
        meeting_types = MeetingType.objects.all()
        serializer = CategorySerializer(meeting_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        meeting_type = MeetingType.objects.create(
            name=request.data["name"]
        )

        serializer = CategorySerializer(meeting_type)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):

        meeting_type = MeetingType.objects.get(pk=pk)
        meeting_type.name = request.data["name"]
        meeting_type.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        meeting_type = MeetingType.objects.get(pk=pk)
        meeting_type.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingType
        fields = ("id", "name")

"""View module for handling requests for boards"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from jobseekerapi.models import Tag


class TagView(ViewSet):
    """Board View"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single Board
        Returns:
            Response -- JSON Serialized Board"""
        try:
            tag = Tag.objects.get(pk=pk)
        except:
            return Response(
                {"message": "The tag you requested does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def list(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        tag = Tag.objects.create(
            name=request.data["name"]
        )
        

        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def update(self, request, pk):

        tag = Tag.objects.get(pk=pk)
        tag.name = request.data["name"]
        tag.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        tag = Tag.objects.get(pk=pk)
        tag.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")
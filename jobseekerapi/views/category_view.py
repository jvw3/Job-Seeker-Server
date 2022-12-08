"""View module for handling requests for boards"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from jobseekerapi.models import Category


class CategoryView(ViewSet):
    """Board View"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single Board
        Returns:
            Response -- JSON Serialized Board"""
        try:
            category = Category.objects.get(pk=pk)
        except:
            return Response(
                {"message": "The category you requested does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def list(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        category = Category.objects.create(
            name=request.data["name"]
        )

        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def update(self, request, pk):

        category = Category.objects.get(pk=pk)
        category.name = request.data["name"]
        category.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")

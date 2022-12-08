"""View module for handling requests for boards"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from jobseekerapi.models import Question


class QuestionView(ViewSet):
    """Board View"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single Board
        Returns:
            Response -- JSON Serialized Board"""
        try:
            question = Question.objects.get(pk=pk)
        except:
            return Response(
                {"message": "The question you requested does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def list(self, request):
        companies = Question.objects.all()
        serializer = QuestionSerializer(companies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        question = Question.objects.create(
            content=request.data["content"]
        )

        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def update(self, request, pk):

        category = Question.objects.get(pk=pk)
        category.content = request.data["content"]
        category.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        question = Question.objects.get(pk=pk)
        question.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("id", "content")
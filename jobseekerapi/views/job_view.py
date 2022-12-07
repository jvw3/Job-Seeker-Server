"""View module for handling requests for boards"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from jobseekerapi.models import Job


class JobView(ViewSet):
    """Board View"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single Board
        Returns:
            Response -- JSON Serialized Board"""
        try:
            job = Job.objects.get(pk=pk)
        except:
            return Response(
                {"message": "The job you requested does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = JobSerializer(job)
        return Response(serializer.data)

    def list(self, request):
        companies = Job.objects.all()
        serializer = JobSerializer(companies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        job = Job.objects.create(
            title=request.data["title"]
        )

        serializer = JobSerializer(job)
        return Response(serializer.data)

    def update(self, request, pk):

        job = Job.objects.get(pk=pk)
        job.title = request.data["title"]
        job.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        job = Job.objects.get(pk=pk)
        job.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ("id", "title")
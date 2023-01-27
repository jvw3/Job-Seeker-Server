"""View module for handling requests for boards"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from jobseekerapi.models import BoardJobTag, Board, BoardJob, Tag


class BoardJobTagView(ViewSet):
    """Board View"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single Board
        Returns:
            Response -- JSON Serialized Board"""
        try:
            board_job_tag = BoardJobTag.objects.get(pk=pk)
        except:
            return Response(
                {"message": "The board job tag you requested does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BoardJobTagSerializer(board_job_tag)
        return Response(serializer.data)

    def list(self, request):
        filtered_board_job_tags = BoardJobTag.objects.all()

        if "boardjob" in request.query_params:
            board_query_value = request.query_params["boardjob"]

            try:
                board_job = BoardJob.objects.get(pk=board_query_value)
                filtered_board_job_tags = BoardJobTag.objects.filter(board_job=board_job.id)

            except:
                return Response(
                {"message": "The board job you are searching for does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BoardJobTagSerializer(filtered_board_job_tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        board_job = BoardJob.objects.get(pk=request.data["board_job"])
        tag = Tag.objects.get(pk=request.data["tag"])
        board_job_tags = BoardJobTag.objects.filter(board_job=board_job.id)


        board_job_tag = BoardJobTag()
        board_job_tag.board_job = board_job
        board_job_tag.tag = tag

        for job_tag in board_job_tags:
            if job_tag.tag == board_job_tag.tag:
                return Response(
                {"message": "This tag already exists on your job! Please choose another."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )


        board_job_tag.save()

        serializer = BoardJobTagSerializer(board_job_tag)
        return Response(serializer.data)

    def destroy(self, request, pk):
        board_job_tag = BoardJobTag.objects.get(pk=pk)
        board_job_tag.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")

class BoardJobTagSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=False)

    class Meta:
        model = BoardJobTag
        fields = ("id", "board_job", "tag")

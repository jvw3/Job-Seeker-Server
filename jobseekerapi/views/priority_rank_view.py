"""View module for handling requests for boards"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from jobseekerapi.models import Question, PriorityRank, Board


class PriorityRankView(ViewSet):
    """Priority Rank View"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single Board Priority Rank
        Returns:
            Response -- JSON Serialized Board"""
        try:
            priority_rank = PriorityRank.objects.get(pk=pk)
        except:
            return Response(
                {"message": "The priority rank you requested does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PriorityRankSerializer(priority_rank)
        return Response(serializer.data)

    def list(self, request):
        priority_ranks = PriorityRank.objects.all()

        if "board" in request.query_params:
            query_value = request.query_params["board"]
            found_rankings = PriorityRank.objects.filter(board=query_value).order_by("rank_value")
            serializer = PriorityRankSerializer(found_rankings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


        serializer = PriorityRankSerializer(priority_ranks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        board = Board.objects.get(pk=request.data["board"])

        priority_rank = PriorityRank.objects.create(
            board=board,
            name=request.data["name"],
            rank_value=request.data["rank_value"],
        )

        serializer = PriorityRankSerializer(priority_rank)
        return Response(serializer.data)

    def update(self, request, pk):

        priority_rank = PriorityRank.objects.get(pk=pk)
        board = Board.objects.get(pk=request.data["board"])

        priority_rank.board = board
        priority_rank.name = request.data["name"]
        priority_rank.rank_value = request.data["rank_value"]
        priority_rank.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        question = Question.objects.get(pk=pk)
        question.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class PriorityRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriorityRank
        fields = ("id", "board", "name", "rank_value")
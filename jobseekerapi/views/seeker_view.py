from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from jobseekerapi.models import Seeker, Board
from django.contrib.auth.models import User

class SeekerView(ViewSet):

    def retrieve(self, request, pk):


        seeker = Seeker.objects.get(pk=pk)

        serializer = SeekerSerializer(seeker)
        return Response(serializer.data)


    def list(self, request):


        seekers = Seeker.objects.all().order_by('user__first_name')

        if "current" in request.query_params:
            currentseeker = Seeker.objects.get(user=request.auth.user)
            serializer = SeekerSerializer(currentseeker, many=False)
            return Response(serializer.data)

        serializer = SeekerSerializer(seekers, many=True)
        return Response(serializer.data)


    def update(self, request, pk):

        seeker = Seeker.objects.get(pk=pk)
        user = User.objects.get(pk=seeker.user_id)

        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.username = request.data["username"]
        user.email = request.data["email"]
        seeker.current_role = request.data["current_role"]
        seeker.bio = request.data["bio"]
        seeker.elevator_pitch = request.data["elevator_pitch"]

        user.save()
        seeker.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk):
        seeker = Seeker.objects.get(pk=pk)
        seeker.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class BoardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = ("id", "seeker", "title", "goal", "requirements", "categories", "jobs")


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "is_active")

class SeekerSerializer(serializers.ModelSerializer):

    boards = BoardSerializer(many=True)
    user = UserSerializer(many=False)
    class Meta:
        model = Seeker
        fields = ('id', 'user', "current_role", "full_name", 'bio', "elevator_pitch", "boards", "interviews")
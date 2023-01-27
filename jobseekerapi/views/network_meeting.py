"""View module for handling requests for boards"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from jobseekerapi.models import NetworkMeeting, Contact, MeetingType, Seeker


class NetworkMeetingView(ViewSet):
    """Board View"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single Board
        Returns:
            Response -- JSON Serialized Board"""
        try:
            network_meeting = NetworkMeeting.objects.get(pk=pk)
        except:
            return Response(
                {"message": "The category you requested does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = NetworkMeetingSerializer(network_meeting)
        return Response(serializer.data)

    def list(self, request):
        network_meetings = NetworkMeeting.objects.all()

        if "myschedule" in request.query_params:
            active_network_meetings = network_meetings.filter(is_complete=False)
            filtered_network_meetings = active_network_meetings.order_by("meeting_date")
            serializer = NetworkMeetingSerializer(filtered_network_meetings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if "completed" in request.query_params:
            completed_network_meetings = network_meetings.filter(is_complete=True)
            serializer = NetworkMeetingSerializer(completed_network_meetings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if "scheduled" in request.query_params:
            scheduled_network_meetings = network_meetings.filter(is_complete=False)
            serializer = NetworkMeetingSerializer(scheduled_network_meetings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if "upcoming" in request.query_params:
            seeker = Seeker.objects.get(user=request.auth.user)
            filtered_meetings =  NetworkMeeting.objects.filter(seeker=seeker).order_by("meeting_date")
            if len(filtered_meetings) > 3:
                filtered_meetings = filtered_meetings[0:3]
                serializer = NetworkMeetingSerializer(filtered_meetings, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                serializer = NetworkMeetingSerializer(filtered_meetings, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = NetworkMeetingSerializer(network_meetings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        seeker = Seeker.objects.get(user=request.auth.user)
        contact = Contact.objects.get(pk=request.data["contact"])
        meeting_type = MeetingType.objects.get(pk=request.data["meeting_type"])

        network_meeting = NetworkMeeting.objects.create(
            seeker=seeker,
            contact=contact,
            description=request.data["description"],
            meeting_date=request.data["meeting_date"],
            notes=request.data["notes"],
            is_complete=request.data["is_complete"],
            meeting_type=meeting_type
        )

        serializer = NetworkMeetingSerializer(network_meeting)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):

        meeting_type = NetworkMeeting.objects.get(pk=pk)
        meeting_type.name = request.data["name"]
        meeting_type.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        network_meeting = NetworkMeeting.objects.get(pk=pk)
        network_meeting.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

# class SeekerSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Seeker
#         fields = ('id', "full_name", 'bio', "elevator_pitch", "boards", "interviews")

class ContactSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = Contact
        fields = ("id", "name", "email", "current_role", "current_company", "last_contact", "number_of_contacts", "connection_level", "linked_in", "notes", "seeker")

class NetworkMeetingSerializer(serializers.ModelSerializer):

    contact = ContactSerializer(many=False)
    
    class Meta:
        model = NetworkMeeting
        fields = ("id", "seeker", "contact", "description", "meeting_date", "notes", "is_complete","meeting_type")

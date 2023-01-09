"""View module for handling requests for boards"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from jobseekerapi.models import Seeker, Contact


class ContactView(ViewSet):
    """Contact View"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single Contact
        Returns:
            Response -- JSON Serialized Contact"""
        try:
            contact = Contact.objects.get(pk=pk)
        except:
            return Response(
                {"message": "The contact you requested does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    def list(self, request):
        """ Handle GET requests for all contacts """
        seeker = Seeker.objects.get(user=request.auth.user)
        contacts = Contact.objects.all()
        filtered_contacts =  contacts.filter(seeker=seeker.id)

        # query params that allows users to sort (ascending & descending) their contacts by the following properties: Name, Number Of Contacts, Connection Level, Last Contact Date.
        if "sortby" in request.query_params:
            sort_query_value = request.query_params["sortby"]

            if sort_query_value == "name":
                if "order" in request.query_params:
                    order_query_value = request.query_params["order"]

                    if order_query_value == "asc":
                        ascending_sorted_contact = filtered_contacts.order_by(sort_query_value)
                        serializer = ContactSerializer(ascending_sorted_contact, many=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)

                    elif order_query_value == "desc":
                        descending_sorted_contact = filtered_contacts.order_by(sort_query_value).reverse()
                        serializer = ContactSerializer(descending_sorted_contact, many=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)


            elif sort_query_value == "contactnumber":
                if "order" in request.query_params:
                    order_query_value = request.query_params["order"]

                    if order_query_value == "asc":
                        ascending_sorted_contact = filtered_contacts.order_by("number_of_contacts")
                        serializer = ContactSerializer(ascending_sorted_contact, many=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)

                    elif order_query_value == "desc":
                        descending_sorted_contact = filtered_contacts.order_by("number_of_contacts").reverse()
                        serializer = ContactSerializer(descending_sorted_contact, many=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)

            elif sort_query_value == "connection":
                if "order" in request.query_params:
                    order_query_value = request.query_params["order"]

                    if order_query_value == "asc":
                        ascending_sorted_contact = filtered_contacts.order_by("number_of_contacts")
                        serializer = ContactSerializer(ascending_sorted_contact, many=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)

                    elif order_query_value == "desc":
                        descending_sorted_contact = filtered_contacts.order_by("number_of_contacts").reverse()
                        serializer = ContactSerializer(descending_sorted_contact, many=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)

            elif sort_query_value == "lastcontact":
                if "order" in request.query_params:
                    order_query_value = request.query_params["order"]

                    if order_query_value == "asc":
                        ascending_sorted_contact = filtered_contacts.order_by("last_contact")
                        serializer = ContactSerializer(ascending_sorted_contact, many=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)

                    elif order_query_value == "desc":
                        descending_sorted_contact = filtered_contacts.order_by("last_contact").reverse()
                        serializer = ContactSerializer(descending_sorted_contact, many=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)

        # query params that allows user to search their contact list by name.
        if "name" in request.query_params:
            query_value = request.query_params["name"]
            qv_lowercase = query_value.lower()
            contacts_by_name = []
            for contact in filtered_contacts:
                if qv_lowercase in contact.name.lower():
                    contacts_by_name.append(contact)
            filtered_contacts = contacts_by_name

        # query params that allows users to filter their contacts by their connection level.
        if "connection" in request.query_params:
            query_value = request.query_params["connection"]
            contacts_by_connection = []
            if query_value == "5":
                for contact in filtered_contacts:
                    if contact.connection_level == 5:
                        contacts_by_connection.append(contact)
                serializer = ContactSerializer(contacts_by_connection, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            elif query_value == "4":
                for contact in filtered_contacts:
                    if contact.connection_level == 4:
                        contacts_by_connection.append(contact)
                serializer = ContactSerializer(contacts_by_connection, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            elif query_value == "3":
                for contact in filtered_contacts:
                    if contact.connection_level == 3:
                        contacts_by_connection.append(contact)
                serializer = ContactSerializer(contacts_by_connection, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            elif query_value == "2":
                for contact in filtered_contacts:
                    if contact.connection_level == 2:
                        contacts_by_connection.append(contact)
                serializer = ContactSerializer(contacts_by_connection, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            elif query_value == "1":
                for contact in filtered_contacts:
                    if contact.connection_level == 1:
                        contacts_by_connection.append(contact)
                serializer = ContactSerializer(contacts_by_connection, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            elif query_value == ">3":
                for contact in filtered_contacts:
                    if contact.connection_level > 3:
                        contacts_by_connection.append(contact)
                serializer = ContactSerializer(contacts_by_connection, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            elif query_value == "<3":
                for contact in filtered_contacts:
                    if contact.connection_level < 3:
                        print(contact.connection_level)
                        contacts_by_connection.append(contact)
                serializer = ContactSerializer(contacts_by_connection, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = ContactSerializer(filtered_contacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST request for creation of a new contact"""

        seeker = Seeker.objects.get(user=request.auth.user)
        
        required_contact_fields = ['name', 'current_role', 'current_company', 'last_contact', 'number_of_contacts', 'connection_level', "linked_in", "notes"]
        
        missing_fields = "The following fields are missing from the post request for this contact: "
        is_field_missing = False
        
        for field in required_contact_fields:
            value = request.data.get(field, None)
            if value is None:
                missing_fields += f'{field}, '
                is_field_missing = True

        if is_field_missing:
            return Response({"message": missing_fields}, status = status.HTTP_400_BAD_REQUEST)

        contact = Contact.objects.create(
            name=request.data["name"],
            current_role = request.data["current_role"],
            current_company = request.data["current_company"],
            last_contact = request.data["last_contact"],
            number_of_contacts = request.data["number_of_contacts"],
            connection_level = request.data["connection_level"],
            linked_in = request.data["linked_in"],
            notes = request.data["notes"],
            seeker=seeker
        )

        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT request for update of an existing contact"""
        contact = Contact.objects.get(pk=pk)
        contact.name = request.data["name"]
        contact.current_role = request.data["current_role"]
        contact.current_company = request.data["current_company"]
        contact.last_contact = request.data["last_contact"]
        contact.number_of_contacts = request.data["number_of_contacts"]
        contact.connection_level = request.data["connection_level"]
        contact.linked_in = request.data["linked_in"]
        contact.notes = request.data["notes"]
        contact.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE Request for delete request of an existing contact"""
        contact = Contact.objects.get(pk=pk)
        contact.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class SeekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seeker
        fields = ("id","current_role", "elevator_pitch")

class ContactSerializer(serializers.ModelSerializer):

    seeker = SeekerSerializer(many=False)
    class Meta:
        model = Contact
        fields = ("id", "name", "email", "current_role", "current_company", "last_contact", "number_of_contacts", "connection_level", "linked_in", "notes", "seeker"  )
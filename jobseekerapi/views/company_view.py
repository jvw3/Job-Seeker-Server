"""View module for handling requests for boards"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from jobseekerapi.models import Company


class CompanyView(ViewSet):
    """Board View"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single Board
        Returns:
            Response -- JSON Serialized Board"""
        try:
            company = Company.objects.get(pk=pk)
        except:
            return Response(
                {"message": "The company you requested does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CompanySerializer(company)
        return Response(serializer.data)

    def list(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        company = Company.objects.create(
            name=request.data["name"]
        )

        serializer = CompanySerializer(company)
        return Response(serializer.data)

    def update(self, request, pk):

        category = Company.objects.get(pk=pk)
        category.name = request.data["name"]
        category.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        company = Company.objects.get(pk=pk)
        company.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "name")

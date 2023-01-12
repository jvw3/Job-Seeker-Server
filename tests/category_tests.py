import json
from rest_framework import status
from rest_framework.test import APITestCase
from jobseekerapi.models import Board, Seeker, Category
from rest_framework.authtoken.models import Token
from datetime import date, datetime


class CategoryTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['categories','board_categories', 'board_jobs', 'boards', 'categories', 'companies', 'contacts', 'custom_preps', 'interview_preps', 'interviews', 'jobs', 'meeting_types', 'network_meetings', 'prep_questions', 'priority_rank', 'questions', 'seekers', 'tags', 'tokens', 'users']

    def setUp(self):
        self.seeker = Seeker.objects.first()
        token = Token.objects.get(user=self.seeker.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_category(self):
        """
        Ensure we can create a new Board.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/categories"

        # Define the request body
        data = {
            "name": "Dream Job"
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["name"], "Dream Job" )


    def test_get_category(self):
        """
        Ensure we can get an existing category.
        """

        # Seed the database with a game
        category = Category()
        category.name = "Dream Job"

        category.save()

        # Initiate request and store response
        response = self.client.get(f"/categories/{category.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["name"], "Dream Job" )


    def test_change_category(self):
        """
        Ensure we can change an existing game.
        """
        category = Category()
        category.name = "Dream Job"
        category.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "name": "Fun Job"
        }

        response = self.client.put(f"/categories/{category.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET game again to verify changes were made
        response = self.client.get(f"/categories/{category.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
        self.assertEqual(json_response["name"], "Fun Job" )
        

    def test_delete_category(self):
        """
        Ensure we can delete an existing category.
        """
        category = Category()
        category.name = "Dream Job"
        category.save()

        # DELETE the game you just created
        response = self.client.delete(f"/categories/{category.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the game again to verify you get a 404 response
        response = self.client.get(f"/categories/{category.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

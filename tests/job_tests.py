import json
from rest_framework import status
from rest_framework.test import APITestCase
from jobseekerapi.models import Board, Seeker, Job
from rest_framework.authtoken.models import Token
from datetime import date, datetime


class JobTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['board_categories', 'board_jobs', 'boardjob_tags', 'boards', 'categories', 'companies', 'contacts', 'custom_preps', 'interview_preps', 'interviews', 'jobs', 'meeting_types', 'network_meetings', 'prep_questions', 'priority_rank', 'questions', 'seekers', 'tags', 'tokens', 'users']

    def setUp(self):
        self.seeker = Seeker.objects.first()
        token = Token.objects.get(user=self.seeker.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_job(self):
        """
        Ensure we can create a new job.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/jobs"

        # Define the request body
        data = {
            "title": "QA Engineer"
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the job was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["title"], "QA Engineer" )


    def test_get_job(self):
        """
        Ensure we can get an existing job.
        """

        # Seed the database with a game
        job = Job()
        job.title = "QA Engineer"

        job.save()

        # Initiate request and store response
        response = self.client.get(f"/jobs/{job.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["title"], "QA Engineer" )


    def test_change_job(self):
        """
        Ensure we can change an existing game.
        """
        job = Job()
        job.title = "QA Engineer"
        job.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "title": "Software Intern"
        }

        response = self.client.put(f"/jobs/{job.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET game again to verify changes were made
        response = self.client.get(f"/jobs/{job.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
        self.assertEqual(json_response["title"], "Software Intern" )


    def test_delete_job(self):
        """
        Ensure we can delete an existing job.
        """
        job = Job()
        job.name = "Apple"
        job.save()

        # DELETE the game you just created
        response = self.client.delete(f"/jobs/{job.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the game again to verify you get a 404 response
        response = self.client.get(f"/jobs/{job.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

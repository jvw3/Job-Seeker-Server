import json
from rest_framework import status
from rest_framework.test import APITestCase
from jobseekerapi.models import Board, Seeker
from rest_framework.authtoken.models import Token
from datetime import date, datetime


class ContactTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['board_categories', 'board_jobs', 'boardjob_tags', 'boards', 'categories', 'companies', 'contacts', 'custom_preps', 'interview_preps', 'interviews', 'jobs', 'meeting_types', 'network_meetings', 'prep_questions', 'priority_rank', 'questions', 'seekers', 'tags', 'tokens', 'users']

    def setUp(self):
        self.seeker = Seeker.objects.first()
        token = Token.objects.get(user=self.seeker.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_board(self):
        """
        Ensure we can create a new Board.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/boards"

        # Define the request body
        data = {
            "seeker": {
                "id": 1
                },
            "title": "New Board",
            "goal": "New Job",
            "requirements": "great team",
            "date_started": date.today(),
            "date_ended": "",
            "is_active": False,
            "categories": [ 1, 4 ]
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        today = date.today()
        today_str = today.strftime("%Y-%m-%d")

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["seeker"]["id"], 1 )
        self.assertEqual(json_response["title"], "New Board")
        self.assertEqual(json_response["goal"], "New Job")
        self.assertEqual(json_response["requirements"], "great team")
        self.assertEqual(json_response["date_started"], today_str)
        self.assertEqual(json_response["date_ended"], None)
        self.assertEqual(json_response["is_active"], False)
        self.assertEqual(json_response["categories"], [{'id': 1, 'name': 'Wishlist'}, {'id': 4, 'name': 'Interviewed'}])
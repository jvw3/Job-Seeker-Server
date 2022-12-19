#!/bin/bash

rm db.sqlite3
rm -rf ./jobseekerapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations jobseekerapi
python3 manage.py migrate jobseekerapi
python3 manage.py loaddata users
python3 manage.py loaddata seekers
python3 manage.py loaddata tokens
python3 manage.py loaddata questions
python3 manage.py loaddata companies
python3 manage.py loaddata categories
python3 manage.py loaddata jobs
python3 manage.py loaddata tags
python3 manage.py loaddata boards
python3 manage.py loaddata board_jobs
python3 manage.py loaddata interview_preps
python3 manage.py loaddata interviews
python3 manage.py loaddata custom_preps
python3 manage.py loaddata prep_questions
python3 manage.py loaddata priority_rank
python3 manage.py loaddata board_categories
python3 manage.py loaddata boardjob_tags

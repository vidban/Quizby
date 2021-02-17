"""Generate CSVs of random data for Quizby."""

import csv
from random import choice, randint, sample
from itertools import permutations
import requests
from faker import Faker
from helpers import get_random_datetime

USERS_CSV_HEADERS = ['username', 'email',
                     'password', 'firstname', 'lastname', 'image_url', 'date_joined']
QUESTIONS_CSV_HEADERS = ['question', 'mult_choice', 'user_id',
                         'category', 'private', 'created_on']


NUM_USERS = 10
NUM_QUESTIONS = 100

fake = Faker()

# Generate random profile image URLs to use for users

image_urls = [
    f"https://randomuser.me/api/portraits/{kind}/{i}.jpg"
    for kind, count in [("lego", 10), ("men", 100), ("women", 100)]
    for i in range(count)
]

with open('generator/users.csv', 'w') as users_csv:
    users_writer = csv.DictWriter(users_csv, fieldnames=USERS_CSV_HEADERS)
    users_writer.writeheader()

    for i in range(NUM_USERS):
        users_writer.writerow(dict(
            username=fake.user_name(),
            email=fake.email(),
            password='$2b$12$Q1PUFjhN/AWRQ21LbGYvjeLpZZB6lfZ1BPwifHALGO6oIbyC3CmJe',
            firstname=fake.first_name(),
            lastname=fake.last_name(),
            image_url=choice(image_urls),
            date_joined=get_random_datetime(),
        ))

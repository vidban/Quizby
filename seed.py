from csv import DictReader
from app import app
from models import db, User, Question

db.drop_all()
db.create_all()

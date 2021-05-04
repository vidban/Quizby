from app import app
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Quiz

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres:pgwebdev@localhost:5432/quizby_test"


app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

db.create_all()


class ModelsTestCase(TestCase):
    """Tests for defined models"""

    def setUp(self):
        """Make demo data"""

        db.drop_all()
        db.create_all()

    def tearDown(self):
        """Clean up fouled transactions"""

        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic model work"""

        u = User(
            email="a@b.com",
            username="ab",
            password="abpassword"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no questions, quizzes or activities
        self.assertEqual(len(u.questions), 0)
        self.assertEqual(len(u.quizzes), 0)
        self.assertEqual(len(u.activities), 0)

    def test_valid_signup(self):
        u_test = User.signup("cd", "c@d.com", "cdpassword")
        uid = 999
        u_test.id = uid
        db.session.commit()

        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "cd")
        self.assertEqual(u_test.email, "c@d.com")

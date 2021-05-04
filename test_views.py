from app import app
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Quiz

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres:pgwebdev@localhost:5432/quizby_test"


app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class viewsTestCase(TestCase):
    """Test views"""

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(
            "testuser", "testuser@test.com.com", "testuserpassword")

        self.testuser_id = 999
        self.testuser.id = self.testuser_id

        db.session.commit()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_login_logout(self):
        """Test login and logout route"""
        with self.client as c:
            u = {"username": "testuser", "password": "testuserpassword"}
            res = c.post("/login", data=u, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Dashboard", html)

            res = c.get("/logout", follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertNotIn("Dashboard", html)

    def test_user_profile(self):
        """ Test user profile route"""
        with self.client as c:
            """Test that route not allowed if user not signed in"""
            res = c.get("/users/profile", follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertIn("Access unauthorized.", html)

            u = {"username": "testuser", "password": "testuserpassword"}
            c.post("/login", data=u, follow_redirects=True)

            res = c.get("/users/profile", follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Your Account.", html)

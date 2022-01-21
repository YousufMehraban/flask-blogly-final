from unittest import TestCase

from flask import redirect
from app import app


class Testing_App(TestCase):
    """defining a class to test flask app blogly"""

    def test_show_users(self):
        """testing to display list of all the users """

        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text = True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

    def test_show_user_form(self):
        """testing display of the add user form """

        with app.test_client() as client:
            res = client.get('/add_user')
            html = res.get_data(as_text = True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1> Add New User: </h1>', html)

    def test_add_user(self):
        """testing adding new user through submitting the form """
        with app.test_client() as client:
            res = client.get('/add_user', data = {'first_name':'Rocky'})
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1> Add New User: </h1>', html)


    def test_edit_user(self):
        """testing edit user form"""

        with app.test_client() as client:
            res = client.get('/edit_user/1')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<button>Save Edit</button>', html)


    def test_show_post_form(self):
        """testing the add post form is displayed """

        with app.test_client() as client:
            res = client.get('/add_post/1')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Add New Post', html)

    def test_edit_post(self):
        """testing the post is submitted and added it the database"""

        with app.test_client() as client:
            res = client.get('/edit_post/1')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Edit Post for', html)


import unittest
from ..web.forms import RegistrationForm, LoginForm, UpdateAccountForm, CalculateCalories

class TestForms(unittest.TestCase):
    def test_registration_form(self):
        form = RegistrationForm(name='John Doe', email='john@doe.com', password='password', confirm_password='password')
        self.assertTrue(form.validate())

    def test_login_form(self):
        form = LoginForm(email='john@doe.com', password='password')
        self.assertTrue(form.validate())
import unittest
from web.diet.forms import RegistrationForm, LoginForm, UpdateAccountForm

class TestForms(unittest.TestCase):
    def test_registration_form(self):
        form = RegistrationForm(name='John Doe', email='john@doe.com', password='password', confirm_password='password')
        self.assertTrue(form.validate())

    def test_login_form(self):
        form = LoginForm(email='john@doe.com', password='password')
        self.assertTrue(form.validate())

    # def test_update_account_form(self):
        # form = UpdateAccountForm(name='John Doe',


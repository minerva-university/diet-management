import pytest
from wtforms.validators import ValidationError
from web.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    CalculateCalories,
    RequestResetForm,
    ResetPasswordForm,
    WeightTimeFilterForm,
    CaloriesTimeFilterForm,
)
from web.models import User
from web import app  # imports the Flask app instance

# Mock data for testing
users = [
    User(id=1, name="Test User", email="test@example.com", password="testpassword"),
    User(id=2, name="Another User", email="another@example.com", password="anotherpassword"),
]

# Fixture to mock User query
@pytest.fixture
def mock_user_query(monkeypatch):
    def mock_filter_by(*args, **kwargs):
        return mock_first

    monkeypatch.setattr(User, "query", lambda: None)
    monkeypatch.setattr(User.query, "filter_by", mock_filter_by)

def mock_first(*args, **kwargs):
    email = kwargs["email"]
    for user in users:
        if user.email == email:
            return user
    return None

def test_registration_form_validates_email(mock_user_query):
    form = RegistrationForm(email="test@example.com")
    with pytest.raises(ValidationError, match="That email is taken. Please choose a different one."):
        form.validate_email(form.email)

def test_login_form():
    with app.app_context():  # create an application context for the test
        form = LoginForm(email="test@example.com", password="testpassword")
        assert form.email.data == "test@example.com"
        assert form.password.data == "testpassword"

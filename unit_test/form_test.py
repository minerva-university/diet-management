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

# Mock data for testing
users = [
    User(id=1, name="Test User", email="test@example.com", password="testpassword"),
    User(id=2, name="Another User", email="another@example.com", password="anotherpassword"),
]

# Utility function for mocking query results
def mock_first(*args, **kwargs):
    email = kwargs["email"]
    for user in users:
        if user.email == email:
            return user
    return None

# Fixture to mock User query
@pytest.fixture
def mock_user_query(monkeypatch):
    monkeypatch.setattr(User, "query", lambda: None)
    monkeypatch.setattr(User.query, "filter_by", lambda **kwargs: None)
    monkeypatch.setattr(User.query.filter_by, "first", mock_first)

def test_registration_form_validates_email(mock_user_query):
    form = RegistrationForm(email="test@example.com")
    with pytest.raises(ValidationError, match="That email is taken. Please choose a different one."):
        form.validate_email(form.email)

def test_login_form():
    form = LoginForm(email="test@example.com", password="testpassword")
    assert form.email.data == "test@example.com"
    assert form.password.data == "testpassword"

# Add tests for the remaining forms following a similar pattern

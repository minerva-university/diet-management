import pytest
from web import app, db
from web.models import User
from web.forms import LoginForm

class TestLoginForm(LoginForm):
    __test__ = False
    class Meta:
        csrf = False

class MockQuery:
    def filter_by(self, **kwargs):
        return mock_first

@pytest.fixture
def mock_user_query(monkeypatch):
    """
    Mock the User.query object to return a mock user
    """
    mock_query = MockQuery()
    monkeypatch.setattr(User, "query", mock_query)

def mock_first():
    """
    Creates a mock user

    Returns:
        User: A mock user
    """
    user = User(id=1, name="testuser", email="test@example.com")
    user.set_password("testpassword")
    return user

def test_login_form_valid_credentials(mock_user_query):
    """
    Tests if the login form validates with valid credentials

    Params:
        mock_user_query: A mock user query

    Returns:
        None
    """
    with app.test_request_context():  # create a request context
        with app.app_context():  # create an application context
            form = TestLoginForm(email="test@example.com", password="password")
            validation_result = form.validate()
            assert validation_result == True


def test_login_form_invalid_credentials(mock_user_query):
    """
    Tests if the login form validates with invalid credentials

    Params:
        mock_user_query: A mock user query

    Returns:
        None
    """
    with app.test_request_context():  # create a request context
        with app.app_context():  # create an application context
            form = LoginForm(email="test@example.com", password="wrongpassword")
            assert form.validate() == False

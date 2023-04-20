import pytest
from web import app, db
from web.models import User
from web.forms import LoginForm

class TestLoginForm(LoginForm):
    """
    A test version of the login form
    """
    __test__ = False
    class Meta:
        csrf = False

class MockQuery:
    """
    A mock query object. This is used to mock the query object returned by the User model
    """
    def filter_by(self, **kwargs):
        return mock_first

@pytest.fixture
def mock_user_query(monkeypatch):
    """
    A fixture that mocks the User model query object.

    Params:
        monkeypatch: A pytest fixture that allows us to mock objects

    Returns:
        None
    """
    mock_query = MockQuery()
    monkeypatch.setattr(User, "query", mock_query)

def mock_first():
    """
    A mock function that returns a test user
    """
    user = User(id=1, username="testuser", email="test@example.com")
    user.set_password("testpassword")
    return user

def test_login_form_valid_credentials(mock_user_query):
    """
    Test that the login form validates correctly when the credentials are correct

    Params:
        mock_user_query: A pytest fixture that mocks the User model query object

    Returns:
        None
    """
    with app.test_request_context():  # create a request context
        with app.app_context():  # create an application context
            form = TestLoginForm(email="test@example.com", password="password")
            validation_result = form.validate()
            print("Form errors:", form.errors)
            assert validation_result == True


def test_login_form_invalid_credentials(mock_user_query):
    """
    Test that the login form validates correctly when the credentials are incorrect

    Params:
        mock_user_query: A pytest fixture that mocks the User model query object

    Returns:
        None
    """
    with app.test_request_context():  # create a request context
        with app.app_context():  # create an application context
            form = LoginForm(email="test@example.com", password="wrongpassword")
            assert form.validate() == False

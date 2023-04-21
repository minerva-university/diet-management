import pytest
from web import app, db
from web.models.User import User
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
    mock_query = MockQuery()
    monkeypatch.setattr(User, "query", mock_query)

def mock_first():
    user = User(id=1, name="testuser", email="test@example.com")
    user.set_password("testpassword")
    return user

def test_login_form_valid_credentials(mock_user_query):
    with app.test_request_context():  # create a request context
        with app.app_context():  # create an application context
            form = TestLoginForm(email="test@example.com", password="password")
            validation_result = form.validate()
            print("Form errors:", form.errors)
            assert validation_result == True


def test_login_form_invalid_credentials(mock_user_query):
    with app.test_request_context():  # create a request context
        with app.app_context():  # create an application context
            form = LoginForm(email="test@example.com", password="wrongpassword")
            assert form.validate() == False

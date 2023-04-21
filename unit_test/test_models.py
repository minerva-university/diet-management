import pytest
from sqlalchemy.exc import IntegrityError
from web import db, app
from web.models import User, UserWeightOverTime, UserCaloriesOverTime, UserCalories, UserHistory, Meals, MealsPhotos, MealsLabel, UserCurrentDiet, UserCurrentDietMeals, DietCalories

@pytest.fixture(scope='module')
def test_app():
    """
    Create a test client for the app
    """
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_create_user(test_app):
    """
    Test creating a user

    Params:
        test_app: A test app

    Returns:
        None
    """
    user = User(name='John Doe', email='john.doe@example.com', password='testpassword')
    db.session.add(user)
    db.session.commit()

    fetched_user = User.query.filter_by(email='john.doe@example.com').first()
    assert fetched_user is not None
    assert fetched_user.name == 'John Doe'
    assert fetched_user.email == 'john.doe@example.com'
    assert fetched_user.password == 'testpassword'


def test_user_weight_over_time(test_app):
    """
    Test creating a user weight over time object

    Params:
        test_app: A test app

    Returns:
        None
    """
    user = User(name='John Doe', email='john.doe@example.com', password='testpassword')
    db.session.add(user)
    db.session.commit()

    user_weight = UserWeightOverTime(user_id=user.id, weight=80)
    db.session.add(user_weight)
    db.session.commit()

    fetched_user_weight = UserWeightOverTime.query.filter_by(user_id=user.id).first()
    assert fetched_user_weight is not None
    assert fetched_user_weight.weight == 80
    assert fetched_user_weight.user == user


def test_user_calories(test_app):
    """
    Test creating a user calories object

    Params:
        test_app: A test app

    Returns:
        None
    """
    user = User(name='John Doe', email='john.doe@example.com', password='testpassword')
    db.session.add(user)
    db.session.commit()

    user_calories = UserCalories(user_id=user.id, calories=2500)
    db.session.add(user_calories)
    db.session.commit()

    fetched_user_calories = UserCalories.query.filter_by(user_id=user.id).first()
    assert fetched_user_calories is not None
    assert fetched_user_calories.calories == 2500
    assert fetched_user_calories.user == user

def test_user_history(test_app):
    """
    Test creating a user history object

    Params:
        test_app: A test app

    Returns:
        None
    """
    user = User(name='John Doe', email='john.doe@example.com', password='testpassword')
    db.session.add(user)
    db.session.commit()

    user_history = UserHistory(user_id=user.id, weight=80, height=180, age=25, activity_level='Moderately Active', gender='Male', goal='Lose Weight')
    db.session.add(user_history)
    db.session.commit()

    fetched_user_history = UserHistory.query.filter_by(user_id=user.id).first()
    assert fetched_user_history is not None
    assert fetched_user_history.weight == 80
    assert fetched_user_history.height == 180
    assert fetched_user_history.age == 25
    assert fetched_user_history.activity_level == 'Moderately Active'
    assert fetched_user_history.gender == 'Male'
    assert fetched_user_history.goal == 'Lose Weight'
    assert fetched_user_history.user == user


# To be continued

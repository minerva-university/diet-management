import pytest
from sqlalchemy.exc import IntegrityError
from web import db, app
from web.models.User import User
from web.models.UserWeightOverTime import UserWeightOverTime
from web.models.UserCaloriesOverTime import UserCaloriesOverTime
from web.models.UserCalories import UserCalories
from web.models.UserHistory import UserHistory
from web.models.Meals import Meals
from web.models.MealsPhotos import MealsPhotos
from web.models.MealsLabel import MealsLabel
from web.models.UserCurrentDiet import UserCurrentDiet
from web.models.UserCurrentDietMeals import UserCurrentDietMeals
from web.models.DietCalories import DietCalories

@pytest.fixture(scope='module')
def test_app():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_create_user(test_app):
    user = User(name='John Doe', email='john.doe@example.com', password='testpassword')
    db.session.add(user)
    db.session.commit()

    fetched_user = User.query.filter_by(email='john.doe@example.com').first()
    assert fetched_user is not None
    assert fetched_user.name == 'John Doe'
    assert fetched_user.email == 'john.doe@example.com'
    assert fetched_user.password == 'testpassword'


def test_user_weight_over_time(test_app):
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

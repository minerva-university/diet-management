import pytest
from web import app, db
from web.models import User, UserWeightOverTime, UserCalories
from web.urls import calculate_calories

@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    test_client = app.test_client()

    with app.app_context():
        db.create_all()

    yield test_client

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def test_user():
    email = 'testuser@example.com'
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        db.session.delete(existing_user)
        db.session.commit()

    user = User(name='TestUser', email=email, password='testpassword')
    db.session.add(user)
    db.session.commit()
    yield user
    db.session.delete(user)
    db.session.commit()

def test_calculate_calories(test_user):
    test_user.gender = 'Male'
    test_user.age = 30
    test_user.height = 180
    test_user.weight = 80
    test_user.goal = 'Maintain Weight'
    test_user.activity_level = 'Sedentary'

    calories = calculate_calories(test_user)
    assert calories == 2237

def test_account_calories_update(test_user):
    test_user.gender = 'Male'
    test_user.age = 30
    test_user.height = 180
    test_user.weight = 80
    test_user.goal = 'Maintain Weight'
    test_user.activity_level = 'Sedentary'
    db.session.commit()

    with app.app_context():
        calories = calculate_calories(test_user)
        UserCalories.query.filter_by(user_id=test_user.id).delete()
        user_calories = UserCalories(calories=calories, user_id=test_user.id)
        db.session.add(user_calories)
        db.session.commit()

        calories_from_db = UserCalories.query.filter_by(user_id=test_user.id).first().calories
        assert calories == calories_from_db

        test_user.weight = 85
        test_user.goal = 'Lose Weight'
        test_user.activity_level = 'Moderately Active'
        db.session.commit()

        updated_calories = calculate_calories(test_user)
        UserCalories.query.filter_by(user_id=test_user.id).delete()
        updated_user_calories = UserCalories(calories=updated_calories, user_id=test_user.id)
        db.session.add(updated_user_calories)
        db.session.commit()

        updated_calories_from_db = UserCalories.query.filter_by(user_id=test_user.id).first().calories
        assert updated_calories == updated_calories_from_db
        assert calories != updated_calories_from_db

def test_account_weight_history(test_user):
    test_user.height = 180
    test_user.weight = 80
    db.session.commit()

    with app.app_context():
        initial_weight = test_user.weight
        weight_over_time = UserWeightOverTime(user_id=test_user.id, weight=initial_weight)
        db.session.add(weight_over_time)
        db.session.commit()

        weight_history = UserWeightOverTime.query.filter_by(user_id=test_user.id).all()
        assert len(weight_history) == 1
        assert weight_history[0].weight == 80

        test_user.weight = 85
        db.session.commit()

        updated_weight = test_user.weight
        weight_over_time = UserWeightOverTime(user_id=test_user.id, weight=updated_weight)
        db.session.add(weight_over_time)
        db.session.commit()

        updated_weight_history = UserWeightOverTime.query.filter_by(user_id=test_user.id).all()
        assert len(updated_weight_history) == 2
        assert updated_weight_history[1].weight == 85

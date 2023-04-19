import pytest
from sqlalchemy.exc import IntegrityError
from web import db, app
from web.models import User, UserWeightOverTime, UserCaloriesOverTime, UserCalories, UserHistory, Meals, MealsPhotos, MealsLabel, UserCurrentDiet, UserCurrentDietMeals, DietCalories

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

def test_create_user_with_duplicate_email(test_app):
    user1 = User(name='John Doe', email='john.doe@example.com', password='testpassword')
    user2 = User(name='Jane Doe', email='john.doe@example.com', password='testpassword')
    db.session.add(user1)
    db.session.commit()

    with pytest.raises(IntegrityError):
        db.session.add(user2)
        db.session.commit()

def test_user_get_bmi(test_app):
    user = User(name='John Doe', email='john.doe@example.com', password='testpassword', weight=80, height=180)
    db.session.add(user)
    db.session.commit()

    fetched_user = User.query.filter_by(email='john.doe@example.com').first()
    assert fetched_user.get_bmi == round(80 / (180 / 100) ** 2, 2)

# To be continued

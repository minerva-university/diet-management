import os
# Set the DATABASE_URL environment variable to use SQLite test database
os.environ['DATABASE_URL'] = 'sqlite:///test.db'
import pytest
from web import app, db
from web.models import User, Meals, UserCalories, MealsLabel
from web.meal_planner import choose_meals_for_user

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
    user = User(name='TestUser', email='testuser@example.com', password='testpassword')
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def test_meals():
    meals = [
        Meals(name='Breakfast Meal 1', calories=100, serving_size=1, recipe='Recipe'),
        Meals(name='Breakfast Meal 2', calories=200, serving_size=1, recipe='Recipe'),
        Meals(name='Lunch Meal 1', calories=300, serving_size=1, recipe='Recipe'),
        Meals(name='Lunch Meal 2', calories=400, serving_size=1, recipe='Recipe'),
        Meals(name='Dinner Meal 1', calories=500, serving_size=1, recipe='Recipe'),
        Meals(name='Dinner Meal 2', calories=600, serving_size=1, recipe='Recipe')
    ]
    meals_labels = [
        MealsLabel(meal_id=1, label='breakfast'),
        MealsLabel(meal_id=2, label='breakfast'),
        MealsLabel(meal_id=3, label='lunch'),
        MealsLabel(meal_id=4, label='lunch'),
        MealsLabel(meal_id=5, label='dinner'),
        MealsLabel(meal_id=6, label='dinner')
    ]

    for meal in meals:
        db.session.add(meal)
    for meal_label in meals_labels:
        db.session.add(meal_label)
    db.session.commit()

    return meals

def test_choose_meals_for_user(test_client, test_user, test_meals):
    user_calories = UserCalories(user_id=test_user.id, calories=2000)
    db.session.add(user_calories)
    db.session.commit()

    (breakfast_meal, _), (lunch_meal, _), (dinner_meal, _) = choose_meals_for_user(test_user.id)

    mock_meals_names = [meal.name for meal in test_meals]
    assert breakfast_meal.name in mock_meals_names, "Breakfast meal not found in the test meals"
    assert lunch_meal.name in mock_meals_names, "Lunch meal not found in the test meals"
    assert dinner_meal.name in mock_meals_names, "Dinner meal not found in the test meals"

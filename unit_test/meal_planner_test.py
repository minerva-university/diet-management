import pytest
from unittest.mock import MagicMock, patch
from web.models import Meals, MealsLabel, UserCalories
from web.meal_planner import choose_meals_for_user


@pytest.fixture
def mock_meals():
    meals = [Meals(id=i, name=f"Meal {i}", calories=i * 100) for i in range(1, 6)]
    return meals


@pytest.fixture
def mock_user_calories():
    return UserCalories(user_id=1, calories=2000)


def test_choose_meals_for_user(mock_meals, mock_user_calories):
    with patch("web.meal_planner.random.uniform", side_effect=[1.0, 1.0, 0.7, 1.3, 0.7, 1.3]) as mock_random_uniform:
        ...
        breakfast_meal, lunch_meal, dinner_meal = choose_meals_for_user(1)
        
        mock_meals_names = [meal.name for meal in mock_meals]

        assert breakfast_meal[0].name in mock_meals_names
        assert lunch_meal[0].name in mock_meals_names
        assert dinner_meal[0].name in mock_meals_names
        assert breakfast_meal[1] >= 0.7 and breakfast_meal[1] <= 1.3
        assert lunch_meal[1] >= 0.7 and lunch_meal[1] <= 1.3
        assert dinner_meal[1] >= 0.7 and dinner_meal[1] <= 1.3

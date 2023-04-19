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
    with patch("web.meal_planner.random.uniform", return_value=1) as mock_random_uniform:
        Meals.query = MagicMock()
        Meals.query.join.return_value = Meals.query
        Meals.query.filter.return_value = Meals.query
        Meals.query.all.return_value = mock_meals
        
        with patch("web.meal_planner.UserCalories.query.filter_by") as mock_filter_by:
            mock_filter_by.return_value.first.return_value = mock_user_calories

            breakfast_meal, lunch_meal, dinner_meal = choose_meals_for_user(1)

            assert breakfast_meal[0] in mock_meals
            assert lunch_meal[0] in mock_meals
            assert dinner_meal[0] in mock_meals
            assert breakfast_meal[1] >= 0.7 and breakfast_meal[1] <= 1.3
            assert lunch_meal[1] >= 0.7 and lunch_meal[1] <= 1.3
            assert dinner_meal[1] >= 0.7 and dinner_meal[1] <= 1.3



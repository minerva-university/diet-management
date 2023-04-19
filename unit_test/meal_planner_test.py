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
        UserCalories.query.filter_by.return_value = MagicMock(first=MagicMock(return_value=mock_user_calories))

        user_id = 1
        meals = choose_meals_for_user(user_id)

        # Assert that the chosen meals are within the allocated calories range
        for meal, serving_factor in meals:
            allocated_calories = meal.calories * serving_factor
            required_calories = mock_user_calories.calories
            assert 0.7 * required_calories / 3 <= allocated_calories <= 1.3 * required_calories / 3

        # Assert that the random.uniform function is called 3 times (for breakfast, lunch, and dinner)
        assert mock_random_uniform.call_count == 3

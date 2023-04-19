from unittest.mock import patch, MagicMock
from web.meal_planner import choose_meals_for_user
from web.models import Meals, UserCalories


class TestMealPlanner:
    mock_meals = [
        Meals('Breakfast Meal 1', 100),
        Meals('Breakfast Meal 2', 200),
        Meals('Lunch Meal 1', 300),
        Meals('Lunch Meal 2', 400),
        Meals('Dinner Meal 1', 500),
        Meals('Dinner Meal 2', 600)
    ]
    mock_user_calories = UserCalories(2000)

    def test_choose_meals_for_user(self):
        with patch("web.meal_planner.random.uniform", side_effect=[1.0, 1.0, 0.7, 1.3, 0.7, 1.3]) as mock_random_uniform:
            Meals.query = MagicMock()
            Meals.query.join.return_value = Meals.query

            def mock_filter(label_expression):
                label = str(label_expression.right)  # Extract the label value
                return [meal for meal in self.mock_meals if label.lower() in meal.name.lower()]

            Meals.query.filter.side_effect = mock_filter
            Meals.query.all.return_value = self.mock_meals

            with patch("web.meal_planner.UserCalories.query.filter_by") as mock_filter_by:
                mock_filter_by.return_value.first.return_value = self.mock_user_calories

                breakfast_meal, lunch_meal, dinner_meal = choose_meals_for_user(1)

                # Assertions
                mock_meals_names = [meal.name for meal in self.mock_meals]
                assert breakfast_meal.name in mock_meals_names, "Breakfast meal not found in the mock meals"
                assert lunch_meal.name in mock_meals_names, "Lunch meal not found in the mock meals"
                assert dinner_meal.name in mock_meals_names, "Dinner meal not found in the mock meals"

                # Check if the total calories for the selected meals are within the required calories
                total_calories = breakfast_meal.calories + lunch_meal.calories + dinner_meal.calories
                required_calories = self.mock_user_calories.calories
                assert 0.7 * required_calories <= total_calories <= 1.3 * required_calories, "Total calories not within the required range"

from unittest.mock import patch, MagicMock
from web.meal_planner import choose_meals_for_user
from web.models import Meals, UserCalories

class TestMealPlanner:
    mock_meals = [
        Meals(name='Breakfast Meal 1', calories=100),
        Meals(name='Breakfast Meal 2', calories=200),
        Meals(name='Lunch Meal 1', calories=300),
        Meals(name='Lunch Meal 2', calories=400),
        Meals(name='Dinner Meal 1', calories=500),
        Meals(name='Dinner Meal 2', calories=600)
    ]
    mock_user_calories = UserCalories(user_id=1, calories=2000)

    def test_choose_meals_for_user(self):
        with patch("web.meal_planner.random.uniform", side_effect=[1.0, 1.0, 0.7, 1.3, 0.7, 1.3]) as mock_random_uniform:
            mock_query = MagicMock()
            Meals.query = mock_query
            mock_query.join.return_value = mock_query
            mock_query.filter.return_value = mock_query
    
            # Define a list of meals that should be returned when the .all() method is called
            mock_query.all.return_value = self.mock_meals
    
            with patch("web.meal_planner.UserCalories.query.filter_by") as mock_filter_by:
                mock_filter_by.return_value.first.return_value = self.mock_user_calories
    
                # Unpack the values returned by the function
                breakfast_meal, lunch_meal, dinner_meal = choose_meals_for_user(1)
    
                # Assertions
                mock_meals_names = [meal.name for meal in self.mock_meals]
                assert breakfast_meal.name in mock_meals_names, "Breakfast meal not found in the mock meals"
                assert lunch_meal.name in mock_meals_names, "Lunch meal not found in the mock meals"
                assert dinner_meal.name in mock_meals_names, "Dinner meal not found in the mock meals"

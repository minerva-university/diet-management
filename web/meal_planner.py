#from web.models import Meals, MealsLabel, UserCalories
from .models.Meals import Meals
from .models.UserCalories import UserCalories
from .models.MealsLabel import MealsLabel
import random  # Import the random module
from logger import info_logger, error_logger

def choose_meals_for_user(user_id):
    # Retrieve the user's required calories
    user_calories = UserCalories.query.filter_by(user_id=user_id).first()
    required_calories = user_calories.calories

    # Allocate the required calories to each meal (breakfast, lunch, dinner)
    breakfast_calories = required_calories * (2/8)
    lunch_calories = required_calories * (3/8)
    dinner_calories = required_calories * (3/8)

    # Add random error (+/- 10%) to the allocated calories for each meal
    breakfast_calories_flexible = random.uniform(0.7, 1.3) * breakfast_calories
    lunch_calories_flexible = random.uniform(0.7, 1.3) * lunch_calories
    dinner_calories_flexible = random.uniform(0.7, 1.3) * dinner_calories

    # Helper function to find the closest meal based on allocated calories
    def find_closest_meal(meals, target_calories):
        closest_meal = min(meals, key=lambda meal: abs(meal.calories - target_calories))
        return closest_meal

    # Retrieve meals for each label category
    breakfast_meals = Meals.query.join(MealsLabel, Meals.id == MealsLabel.meal_id).filter(MealsLabel.label == 'breakfast').all()
    lunch_meals = Meals.query.join(MealsLabel, Meals.id == MealsLabel.meal_id).filter(MealsLabel.label == 'lunch').all()
    dinner_meals = Meals.query.join(MealsLabel, Meals.id == MealsLabel.meal_id).filter(MealsLabel.label == 'dinner').all()

    # Find the closest meal based on allocated calories for each label category
    breakfast_meal = find_closest_meal(breakfast_meals, breakfast_calories_flexible)
    lunch_meal = find_closest_meal(lunch_meals, lunch_calories_flexible)
    dinner_meal = find_closest_meal(dinner_meals, dinner_calories_flexible)

    # Calculate the serving size adjustment factor for each meal based on allocated calories
    breakfast_serving_factor = breakfast_calories / breakfast_meal.calories
    breakfast_serving_factor = round(breakfast_serving_factor, 1)
    lunch_serving_factor = lunch_calories / lunch_meal.calories
    lunch_serving_factor = round(lunch_serving_factor, 1)
    dinner_serving_factor = dinner_calories / dinner_meal.calories
    dinner_serving_factor = round(dinner_serving_factor, 1)

    return (breakfast_meal, breakfast_serving_factor), (lunch_meal,lunch_serving_factor), (dinner_meal, dinner_serving_factor)

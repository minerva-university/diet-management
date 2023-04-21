from .. import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from logger import info_logger, error_logger

class UserCurrentDietMeals(db.Model):
    """
    A class representing the meals associated with a user's current diet.

    Attributes:
        id (int): The unique identifier of this diet-meal association.
        user_current_diet_id (int): The ID of the current diet associated with this meal.
        meal_id (int): The ID of the meal associated with this diet.
        created_at (datetime): The timestamp of when this association was created.
        updated_at (datetime): The timestamp of when this association was last updated.
        serving_size (int): The serving size of this meal for this user's current diet.
        user_current_diet (UserCurrentDiet): The UserCurrentDiet object associated with this meal.
        meal (Meals): The Meals object associated with this diet.
    """
    __tablename__ = 'user_current_diet_meals'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_current_diet_id = db.Column(db.Integer, db.ForeignKey('user_current_diet.id'), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    serving_size = db.Column(db.Integer, nullable=False)
    user_current_diet = db.relationship('UserCurrentDiet', backref='user_current_diet_meals')
    meal = db.relationship('Meals', backref='user_current_diet_meals')

    def __repr__(self):
        return f"UserCurrentDietMeals('{self.id}', '{self.meal_id}')"

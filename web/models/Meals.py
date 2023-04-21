from .. import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from logger import info_logger, error_logger


class Meals(db.Model):
    """
    A model class to represent meals in the database.

    Attributes:
        id (int): The unique identifier for the meal.
        name (str): The name of the meal.
        calories (int): The number of calories in the meal.
        serving_size (int): The serving size of the meal.
        recipe (str): The recipe for the meal.
        created_at (datetime): The timestamp of when the meal was created.
        updated_at (datetime): The timestamp of when the meal was last updated.
    """
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    serving_size = db.Column(db.Integer, nullable=False)
    recipe = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    def __repr__(self):
        return f"Meals('{self.name}', '{self.calories}')"

from .. import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from logger import info_logger, error_logger

class MealsLabel(db.Model):
    """
    A model class to represent a label of a meal.

    Attributes:
        id (int): The unique identifier of the meal label.
        meal_id (int): The ID of the meal that the label belongs to.
        label (str): The text of the label.
        created_at (datetime): The timestamp of when the meal label was created.
        updated_at (datetime): The timestamp of when the meal label was last updated.
        meal (Meals): The meal that the label belongs to, as a relationship.

    Methods:
        __repr__(): Returns a string representation of the meal label, containing its label text.

    """

    __tablename__ = 'meals_label'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
    label = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    meal = db.relationship('Meals', backref='meals_label')

    def __repr__(self):
        return f"MealsLabel('{self.label}')"
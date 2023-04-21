from .. import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from logger import info_logger, error_logger

class UserCalories(db.Model):
    """
    A class used to represent a user's total calories.

    Attributes:
    id (int): The ID of the user's calories.
    user_id (int): The ID of the user that the calories belong to.
    calories (int): The total number of calories consumed by the user.
    created_at (datetime): The date and time when the user's calories were recorded.
    updated_at (datetime): The date and time when the user's calories were last updated.
    user (User): The User object that the calories belong to.
    """

    __tablename__ = 'user_calories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    user = db.relationship('User', backref='user_calories')

    def __repr__(self):
        """
        Return a string representation of the UserCalories object.

        Returns:
        str: The string representation of the UserCalories object.
        """
        return f"UserCalories('{self.id}', '{self.calories}')"
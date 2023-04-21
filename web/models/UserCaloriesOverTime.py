from .. import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from logger import info_logger, error_logger

class UserCaloriesOverTime(db.Model):
    """
    A class used to represent a user's calories over time.

    Attributes:
    id (int): The ID of the user's calories over time.
    user_id (int): The ID of the user that the calories over time belongs to.
    calories (int): The number of calories consumed by the user at the specific time.
    created_at (datetime): The date and time when the calories over time were recorded.
    """

    __tablename__ = 'user_calories_over_time'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    def __repr__(self):
        """
        Return a string representation of the UserCaloriesOverTime object.

        Returns:
        str: The string representation of the UserCaloriesOverTime object.
        """
        return f"UserCaloriesOverTime('{self.id}', '{self.calories}')"

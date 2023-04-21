from .. import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from logger import info_logger, error_logger

class UserWeightOverTime(db.Model):
    """
    A class used to represent a user's weight over time.

    Attributes:
    id (int): The ID of the user's weight over time.
    user_id (int): The ID of the user that the weight over time belongs to.
    weight (float): The weight of the user at the specific time.
    created_at (datetime): The date and time when the weight over time was recorded.
    """

    __tablename__ = 'user_bmi_over_time'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    def __repr__(self):
        """
        Return a string representation of the UserWeightOverTime object.

        Returns:
        str: The string representation of the UserWeightOverTime object.
        """
        return f"UserWeightOverTime('{self.id}', '{self.bmi}')"
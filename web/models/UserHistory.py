from .. import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from logger import info_logger, error_logger


class UserHistory(db.Model):
    """
    This class defines the UserHistory table that contains information about a user's weight, height, age, 
    activity level, gender, and goal over time. The table has a foreign key to the User table.

    Attributes:
        id (int): A unique identifier for each UserHistory instance.
        user_id (int): The user ID associated with this UserHistory instance.
        weight (int): The user's weight at the time this UserHistory instance was created.
        height (int): The user's height at the time this UserHistory instance was created.
        age (int): The user's age at the time this UserHistory instance was created.
        activity_level (enum): The user's activity level at the time this UserHistory instance was created.
        gender (enum): The user's gender at the time this UserHistory instance was created.
        goal (enum): The user's goal at the time this UserHistory instance was created.
        created_at (TIMESTAMP): The date and time when this UserHistory instance was created.
        user (relationship): A reference to the User instance associated with this UserHistory instance.

    Methods:
        __repr__(self): Returns a string representation of a UserHistory instance.

    """
    __tablename__ = 'user_history'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    weight = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    activity_level = db.Column(db.Enum('Sedentary', 'Lightly Active', 'Moderately Active', 'Very Active', 'Extra Active', name="activity_types"), nullable=True)
    gender = db.Column(db.Enum('Male', 'Female', name='gender_types'), nullable=True)
    goal = db.Column(db.Enum('Lose Weight', 'Gain Weight', 'Maintain Weight', name='goal_types'), nullable=True)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    user = db.relationship('User', backref='user_history', lazy=True)

    def __repr__(self):
        return f"UserHistory('{self.id}', '{self.weight}', '{self.height}', '{self.age}', '{self.activity_level}')"

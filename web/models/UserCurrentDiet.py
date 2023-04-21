from .. import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from logger import info_logger, error_logger

class UserCurrentDiet(db.Model):
    """
    A class representing a user's current diet.

    Attributes:
        id (int): The unique identifier of the user's current diet.
        user_id (int): The ID of the user associated with this diet.
        created_at (datetime): The timestamp of when this diet was created.
        updated_at (datetime): The timestamp of when this diet was last updated.
        user (User): The User object associated with this diet.
    """
    __tablename__ = 'user_current_diet'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    user = db.relationship('User', backref='user_current_diet')

    def __repr__(self):
        return f"UserCurrentDiet('{self.id}')"
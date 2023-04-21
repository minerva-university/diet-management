from .. import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from logger import info_logger, error_logger


class MealsPhotos(db.Model):
    """
    A model class to represent a photo of a meal.

    Attributes:
        id (int): The unique identifier of the meal photo.
        meal_id (int): The ID of the meal that the photo belongs to.
        photo (bytes): The binary representation of the photo.
        created_at (datetime): The timestamp of when the meal photo was created.
        updated_at (datetime): The timestamp of when the meal photo was last updated.
        meal (Meals): The meal that the photo belongs to, as a relationship.

    Methods:
        __repr__(): Returns a string representation of the meal photo, containing its ID and photo.

    """

    __tablename__ = 'meals_photos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
    photo = db.Column(db.BLOB, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    meal = db.relationship('Meals', backref='meals_photos')

    def __repr__(self):
        return f"MealsPhotos(''{self.id}', {self.photo}')"
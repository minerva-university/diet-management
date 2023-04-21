from .. import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from logger import info_logger, error_logger


class DietCalories(db.Model):
    """
    Model class for diet_calories table.

    Attributes:
    -----------
        id: Primary key for the table
        user_current_diet_id: Foreign key for the user_current_diet table
        calories: The amount of calories for the user's diet
        created_at: Timestamp for when the record was created
        updated_at: Timestamp for when the record was last updated
        user_current_diet: Relationship to the UserCurrentDiet model
    """

    __tablename__ = 'diet_calories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_current_diet_id = db.Column(db.Integer, db.ForeignKey('user_current_diet.id'), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    user_current_diet = db.relationship('UserCurrentDiet', backref='diet_calories')

    def __repr__(self):
        return f"DietCalories('{self.calories}')"

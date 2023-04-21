from .. import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from logger import info_logger, error_logger

@login_manager.user_loader
def load_user(user_id):
    """
    Load the user object for the given user ID.

    Parameters:
    user_id (int): The user ID.

    Returns:
    User: The User object for the given user ID.
    """
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """
    User model representing a user of the application.

    Attributes:
    id (int): The unique ID of the user.
    name (str): The name of the user.
    email (str): The email of the user.
    password (str): The password of the user.
    image_file (str): The image file path of the user.
    weight (int): The weight of the user.
    height (int): The height of the user.
    age (int): The age of the user.
    activity_level (str): The activity level of the user.
    gender (str): The gender of the user.
    goal (str): The goal of the user.
    created_at (datetime): The date and time the user was created.
    updated_at (datetime): The date and time the user was last updated.
    is_active (bool): Whether the user is active or not.
    weights (list): A list of the UserWeightOverTime objects associated with the user.

    Methods:
    get_reset_token(expires_sec=1800):
        Get a reset token for the user.

        Parameters:
        expires_sec (int): The number of seconds for which the token is valid.

        Returns:
        str: The reset token for the user.
    """

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.Text, nullable=False, default='default.jpg')
    weight = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    activity_level = db.Column(db.Enum('Sedentary', 'Lightly Active', 'Moderately Active', 'Very Active', 'Extra Active', name="activity_types"), nullable=True)
    gender = db.Column(db.Enum('Male', 'Female', name='gender_types'), nullable=True)
    goal = db.Column(db.Enum('Lose Weight', 'Gain Weight', 'Maintain Weight', name='goal_types'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    weights = db.relationship('UserWeightOverTime', backref='user', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        """
        Get a reset token for the user.

        Parameters:
        expires_sec (int): The number of seconds for which the token is valid.

        Returns:
        str: The reset token for the user.
        """
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')


    @staticmethod
    def verify_reset_token(token):
        """
        Verify the reset token for the user.

        Parameters:
        token (str): The reset token to be verified.

        Returns:
        User or None: The User object if the token is valid, None otherwise.
        """
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
            info_logger.info("Token reseted")
        except:
            info_logger.error("Validation not succesful")
            return None
        return User.query.get(user_id)

    def get_id(self):
        """
        Get the ID of the user.

        Returns:
        str: The ID of the user.
        """
        # return user id as unicode
        return str(self.id)

    @property
    def get_bmi(self):
        """
        Calculate and return the BMI (Body Mass Index) of the user.

        Returns:
        float: The calculated BMI.
        """
        return round(self.weight / (self.height / 100) ** 2, 2)

    def __repr__(self):
        """
        Return a string representation of the User object.

        Returns:
        str: The string representation of the User object.
        """
        return f"User('{self.name}', '{self.email}')"
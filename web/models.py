from . import db, login_manager, app
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
    email = db.Column(db.Text, unique=True, nullable=False)
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

class UserCurrentDietMeals(db.Model):
    """
    A class representing the meals associated with a user's current diet.

    Attributes:
        id (int): The unique identifier of this diet-meal association.
        user_current_diet_id (int): The ID of the current diet associated with this meal.
        meal_id (int): The ID of the meal associated with this diet.
        created_at (datetime): The timestamp of when this association was created.
        updated_at (datetime): The timestamp of when this association was last updated.
        serving_size (int): The serving size of this meal for this user's current diet.
        user_current_diet (UserCurrentDiet): The UserCurrentDiet object associated with this meal.
        meal (Meals): The Meals object associated with this diet.
    """
    __tablename__ = 'user_current_diet_meals'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_current_diet_id = db.Column(db.Integer, db.ForeignKey('user_current_diet.id'), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    serving_size = db.Column(db.Integer, nullable=False)
    user_current_diet = db.relationship('UserCurrentDiet', backref='user_current_diet_meals')
    meal = db.relationship('Meals', backref='user_current_diet_meals')

    def __repr__(self):
        return f"UserCurrentDietMeals('{self.id}', '{self.meal_id}')"


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


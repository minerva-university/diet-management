from . import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    
class User(db.Model, UserMixin):
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
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def get_id(self):
        # return user id as unicode
        return str(self.id)
    
    @property
    def get_bmi(self):
        """
        Using the property decorator to make this an attribute that we can caculate dynamically
        """
        return round(self.weight / (self.height / 100) ** 2, 2)
    
    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"
    

class UserWeightOverTime(db.Model):
    __tablename__ = 'user_bmi_over_time'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    def __repr__(self):
        return f"UserWeightOverTime('{self.id}', '{self.bmi}')"
    
class UserCaloriesOverTime(db.Model):
    __tablename__ = 'user_calories_over_time'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    def __repr__(self):
        return f"UserCaloriesOverTime('{self.id}', '{self.calories}')"


class UserCalories(db.Model):
    __tablename__ = 'user_calories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    user = db.relationship('User', backref='user_calories')

    def __repr__(self):
        return f"UserCalories('{self.id}', '{self.calories}')"

class UserHistory(db.Model):
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
    __tablename__ = 'user_current_diet'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    user = db.relationship('User', backref='user_current_diet')

    def __repr__(self):
        return f"UserCurrentDiet('{self.id}')"

class UserCurrentDietMeals(db.Model):
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
    __tablename__ = 'diet_calories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_current_diet_id = db.Column(db.Integer, db.ForeignKey('user_current_diet.id'), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    user_current_diet = db.relationship('UserCurrentDiet', backref='diet_calories')

    def __repr__(self):
        return f"DietCalories('{self.calories}')"

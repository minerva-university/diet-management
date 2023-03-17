from diet import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(200), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)
#     height = db.Column(db.Numeric)
#     weight = db.Column(db.Numeric)
#     age = db.Column(db.Numeric)
#     goal = db.Column(db.String(500))

#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}')"
    
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    weight = db.Column(db.Numeric)
    height = db.Column(db.Numeric)
    age = db.Column(db.Integer)
    activity_level = db.Column(db.Enum('Sedentary', 'Lightly Active', 'Moderately Active', 'Very Active', 'Extra Active'))
    specific_diet = db.Column(db.Enum('None', 'Halal', 'Kosher', 'Vegetarian', 'Vegan', 'Keto'))
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

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
    weight = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    activity_level = db.Column(db.Enum('sedentary', 'lightly active', 'moderately active', 'very active', 'extra active'), nullable=False)
    # activity_level = db.Column(db.Text, nullable=False, checkin = ('sedentary', 'lightly active', 'moderately active', 'very active', 'extra active'))
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
        return f"DietCalories(''{self.id}', {self.calories}')"
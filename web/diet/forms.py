from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange
from diet.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class InitializeAccountForm(FlaskForm):
    height = FloatField('Height (m)', validators=[DataRequired(), NumberRange(min=0.0, max=3.0, message='Height must be between 0.0 and 3.0')])
    weight = FloatField('Weight (kg)', validators=[DataRequired(), NumberRange(min=0.0, max=300.0, message='Weight must be between 0.0 and 300.0')])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=0, max=150, message='Age must be between 0 and 150')])
    activity_level_choices = [('', 'Select your activity level'), ('Sedentary', 'Sedentary'), ('Lightly Active', 'Lightly Active'), ('Moderately Active', 'Moderately Active'), ('Very Active', 'Very Active'), ('Extra Active', 'Extra Active')]
    activity_level = SelectField('Activity level', choices=activity_level_choices, validators=[DataRequired()])
    specific_diet_choices = [('', 'Select your diet type'), ('None', 'None'), ('Halal', 'Halal'), ('Kosher', 'Kosher'), ('Vegetarian', 'Vegetarian'), ('Vegan', 'Vegan'), ('Keto', 'Keto')]
    specific_diet = SelectField('Specific diet', choices=specific_diet_choices, validators=[DataRequired()])
    submit = SubmitField('Submit')

class UpdateAccountForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email', validators=[DataRequired()])
    height = FloatField('Height (m)', validators=[DataRequired(), NumberRange(min=0.0, max=3.0, message='Height must be between 0.0 and 3.0')])
    weight = FloatField('Weight (kg)', validators=[DataRequired(), NumberRange(min=0.0, max=300.0, message='Weight must be between 0.0 and 300.0')])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=0, max=150, message='Age must be between 0 and 150')])
    activity_level_choices = [('', 'Select an option'), ('Sedentary', 'Sedentary'), ('Lightly Active', 'Lightly Active'), ('Moderately Active', 'Moderately Active'), ('Very Active', 'Very Active'), ('Extra Active', 'Extra Active')]
    activity_level = SelectField('Activity level', choices=activity_level_choices, validators=[DataRequired()])
    specific_diet_choices = [('', 'Select your diet type'), ('None', 'None'), ('Halal', 'Halal'), ('Kosher', 'Kosher'), ('Vegetarian', 'Vegetarian'), ('Vegan', 'Vegan'), ('Keto', 'Keto')]
    specific_diet = SelectField('Specific diet', choices=specific_diet_choices, validators=[DataRequired()])
    submit = SubmitField('Submit')
    
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

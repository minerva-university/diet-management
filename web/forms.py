from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, EmailField, PasswordField, SubmitField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange, Email
from .models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    height = FloatField('Height (cm)', validators=[DataRequired(), NumberRange(min=0.0, max=300, message='Height must be between 0.0 and 300')])
    weight = FloatField('Weight (kg)', validators=[DataRequired(), NumberRange(min=0.0, max=300.0, message='Weight must be between 0.0 and 300.0')])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=0, max=150, message='Age must be between 0 and 150')])
    goal_options = [('', 'Select an option'), ('Lose Weight', 'Lose Weight'), ('Maintain Weight', 'Maintain Weight'), ('Gain Weight', 'Gain Weight')]
    goal = SelectField('Goal', choices=goal_options, validators=[DataRequired()])
    activity_level_options = [('', 'Select an option'), ('Sedentary', 'Sedentary'), ('Lightly Active', 'Lightly Active'),
                              ('Moderately Active', 'Moderately Active'), ('Very Active', 'Very Active'), ('Extra Active', 'Extra Active')]
    activity_level = SelectField('Activity Level', choices=activity_level_options, validators=[DataRequired()])
    gender_options = [('', 'Select an option'), ('Male', 'Male'), ('Female', 'Female')]
    gender = SelectField('Gender', choices=gender_options, validators=[DataRequired()])
    submit = SubmitField('Update')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class CalculateCalories(FlaskForm):
    height = FloatField('Height (cm)', validators=[DataRequired(), NumberRange(min=0.0, max=300, message='Height must be between 0.0 and 300')])
    weight = FloatField('Weight (kg)', validators=[DataRequired(), NumberRange(min=0.0, max=300.0, message='Weight must be between 0.0 and 300.0')])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=0, max=150, message='Age must be between 0 and 150')])
    goal_options = [('', 'Select an option'), ('Lose Weight', 'Lose Weight'), ('Maintain Weight', 'Maintain Weight'), ('Gain Weight', 'Gain Weight')]
    goal = SelectField('Goal', choices=goal_options, validators=[DataRequired()])
    activity_level_options = [('', 'Select an option'), ('Sedentary', 'Sedentary'), ('Lightly Active', 'Lightly Active'),
                              ('Moderately Active', 'Moderately Active'), ('Very Active', 'Very Active'), ('Extra Active', 'Extra Active')]
    activity_level = SelectField('Activity Level', choices=activity_level_options, validators=[DataRequired()])
    gender_options = [('', 'Select an option'), ('Male', 'Male'), ('Female', 'Female')]
    gender = SelectField('Gender', choices=gender_options, validators=[DataRequired()])
    submit = SubmitField('Submit')

class RequestResetForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')
        
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class WeightTimeFilterForm(FlaskForm):
    """
    Form to allow the user to choose a timeframe for the graph to show their bmi history
    """
    time_options = [('', 'Select a time period'), ('1 Week', '1 Week'), ('2 Weeks', '2 Weeks'), ('3 Weeks', '3 Weeks'), ('1 Month', '1 Month'), ('3 Months', '3 Months'), ('6 Months', '6 Months'), ('1 Year', '1 Year')]
    time = SelectField('Time Period', choices=time_options, validators=[DataRequired()])
    submit = SubmitField('Show Results')

class CaloriesTimeFilterForm(FlaskForm):
    """
    Form to allow the user to choose a timeframe for the graph to show their calorie intake history
    """
    time_options = [('', 'Select a time period'), ('1 Week', '1 Week'), ('2 Weeks', '2 Weeks'), ('3 Weeks', '3 Weeks'), ('1 Month', '1 Month')]
    time = SelectField('Time Period', choices=time_options, validators=[DataRequired()])
    submit = SubmitField('Show Results')
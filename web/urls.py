import datetime
import secrets
import os
from PIL import Image
from flask import render_template, request, redirect, url_for, flash
from web import app, db, bcrypt, mail
from web.forms import RegistrationForm, LoginForm, UpdateAccountForm, CalculateCalories, RequestResetForm, ResetPasswordForm, BMITimeFilterForm, CaloriesTimeFilterForm
from web.models import User, UserCalories, UserCurrentDiet, UserCurrentDietMeals, Meals, MealsPhotos, MealsLabel, DietCalories, UserBMIOverTime, UserCaloriesOverTime
from flask_login import login_user, current_user, logout_user, login_required
from web.meal_planner import choose_meals_for_user
from functools import wraps
from flask_mail import Message

def account_complete(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if not (current_user.height and current_user.weight and current_user.age and current_user.goal and current_user.activity_level and current_user.gender):
                flash('Please complete your account details.', 'warning')
                return redirect(url_for('finish_account'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.name.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, legend='Sign Up')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            # check if the account is not complete and prompt them to finish it
            if not (current_user.height and current_user.weight and current_user.age and current_user.goal and current_user.activity_level and current_user.gender):
                flash('Please complete your account details.', 'warning')
                return redirect(url_for('finish_account'))
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                flash(f'You have been logged in!', 'success')
                return redirect(url_for('index'))
        else:
            flash(f'Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form, legend='Log In')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# finish setting up the account
@app.route('/finish-account', methods=['GET', 'POST'])
@login_required
def finish_account():
    form = CalculateCalories()
    if form.validate_on_submit():
        current_user.height = form.height.data
        current_user.weight = form.weight.data
        current_user.age = form.age.data
        current_user.goal = form.goal.data
        current_user.activity_level = form.activity_level.data
        current_user.gender = form.gender.data

        # populate the UserBMIOverTime table
        bmi = current_user.calculate_bmi()
        bmi_over_time = UserBMIOverTime(user_id=current_user.id, bmi=bmi)
        db.session.add(bmi_over_time)

        db.session.commit()
        flash('Your account has been initialized!', 'success')
        return redirect(url_for('get_calories'))
    return render_template('finish_account.html', title='Complete Account Details', form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    image_file = url_for('static', filename='images/' + current_user.image_file)
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        bmi_changed = False
        # add to the UserBMIOverTime table if the user has updated their height or weight
        if current_user.height != form.height.data or current_user.weight != form.weight.data:
            bmi_changed = True

        current_user.height = form.height.data
        current_user.weight = form.weight.data
        current_user.age = form.age.data
        current_user.goal = form.goal.data
        current_user.activity_level = form.activity_level.data
        current_user.gender = form.gender.data

        if bmi_changed:
            bmi = current_user.get_bmi
            bmi_over_time = UserBMIOverTime(user_id=current_user.id, bmi=bmi)
            db.session.add(bmi_over_time)

        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('get_calories'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        if current_user.height: form.height.data = round(current_user.height, 2)
        if current_user.weight: form.weight.data = round(current_user.weight, 2)
        if current_user.age: form.age.data = int(current_user.age)
        if current_user.goal: form.goal.data = current_user.goal
        if current_user.activity_level: form.activity_level.data = current_user.activity_level
        if current_user.gender: form.gender.data = current_user.gender
    return render_template('account.html', title='Account', form=form, image_file=image_file)

# separated so it can be tested easily with unittest
def calculate_calories(current_user):
    """
    Calculates the calories needed for the user based on their activity level and goal

    Parameters:
        current_user (User): The user object
    
    Returns:
        calories (int): The number of calories needed for the user
    """
    if current_user.gender == 'Male':
        BMR = 66.47 + (13.75 * current_user.weight) + (5.003 * current_user.height) - (6.755 * current_user.age)
    if current_user.gender == 'Female':
        BMR = 655.1 + (9.563 * current_user.weight) + (1.85 * current_user.height) - (4.676 * current_user.age)
    
    if current_user.activity_level == 'Sedentary':
        AMR = BMR * 1.2
    elif current_user.activity_level == 'Lightly Active':
        AMR = BMR * 1.375
    elif current_user.activity_level == 'Moderately Active':
        AMR = BMR * 1.55
    elif current_user.activity_level == 'Very Active':
        AMR = BMR * 1.725
    elif current_user.activity_level == 'Extra Active':
        AMR = BMR * 1.9

    if current_user.goal == 'Lose Weight':
        calories = AMR - 500
    elif current_user.goal == 'Maintain Weight':
        calories = AMR
    elif current_user.goal == 'Gain Weight':
        calories = AMR + 500
    
    calories = round(calories)
    return calories


@app.route('/get-calories', methods=['GET'])
@login_required
@account_complete
def get_calories():
    calories = calculate_calories(current_user)
    user_calories = UserCalories(calories=calories, user_id=current_user.id)
    db.session.add(user_calories)
    db.session.commit()
    return render_template('get_calories.html', title='Get Calories', current_user=current_user, calories=calories)
    
    
@app.route('/get-meals', methods=['GET'])
@login_required
@account_complete
def get_meals():
    if not UserCalories.query.filter_by(user_id=current_user.id).first():
        return redirect(url_for('get_calories'))
    breakfast_meal, lunch_meal, dinner_meal = choose_meals_for_user(current_user.id)
    breakfast_meal, breakfast_serving = breakfast_meal
    lunch_meal, lunch_serving = lunch_meal
    dinner_meal, dinner_serving = dinner_meal
    if UserCurrentDiet.query.filter_by(user_id=current_user.id).first():
        user_current_diet = UserCurrentDiet.query.filter_by(user_id=current_user.id).first()
        UserCurrentDietMeals.query.filter_by(user_current_diet_id=user_current_diet.id).delete()
        DietCalories.query.filter_by(user_current_diet_id=user_current_diet.id).delete()
    else:
        user_current_diet = UserCurrentDiet(user_id=current_user.id)
        db.session.add(user_current_diet)
        db.session.commit()
        
    user_current_meals = [
        UserCurrentDietMeals(user_current_diet_id=user_current_diet.id, meal_id=breakfast_meal.id, serving_size=breakfast_serving),
        UserCurrentDietMeals(user_current_diet_id=user_current_diet.id, meal_id=lunch_meal.id, serving_size=lunch_serving),
        UserCurrentDietMeals(user_current_diet_id=user_current_diet.id, meal_id=dinner_meal.id, serving_size=dinner_serving)
    ]
    db.session.add_all(user_current_meals)
    diet_calories = DietCalories(user_current_diet_id=user_current_diet.id, calories=breakfast_meal.calories*breakfast_serving + lunch_meal.calories*lunch_serving + dinner_meal.calories*dinner_serving)
    db.session.add(diet_calories)
    db.session.commit()
    return redirect(url_for('show_meals'))

@app.route('/show-meals', methods=['GET'])
@login_required
@account_complete
def show_meals():
    if UserCurrentDiet.query.filter_by(user_id=current_user.id).first():
        # print("I am there")
        user_current_diet = UserCurrentDiet.query.filter_by(user_id=current_user.id).first()
        user_current_meals = UserCurrentDietMeals.query.filter_by(user_current_diet_id=user_current_diet.id).all()
        meals = []
        servings = []
        for user_current_meal in user_current_meals:
            meal = Meals.query.filter_by(id=user_current_meal.meal_id).first()
            serving_size = user_current_meal.serving_size
            servings.append(serving_size)
            meals.append(meal)
        diet_calories = DietCalories.query.filter_by(user_current_diet_id=user_current_diet.id).first()
        # print(diet_calories, meals)
        return render_template('show_meals.html',
                               title='Get Meals',
                               current_user=current_user,
                               meals=meals,
                               diet_calories=diet_calories,
                               servings=servings,
                               zip=zip,
                               round=round)
    else:
        return redirect(url_for('get_meals'))

@app.route('/save-meal', methods=['GET', 'POST'])
@login_required
@account_complete
def save_calories():
    user_current_diet = UserCurrentDiet.query.filter_by(user_id=current_user.id).first()
    calories = DietCalories.query.filter_by(user_current_diet_id=user_current_diet.id).first()

    # populate the user calories over time table to track and then later plot it over time
    user_calories_over_time = UserCaloriesOverTime(calories=calories.calories, user_id=current_user.id)
    db.session.add(user_calories_over_time)
    db.session.commit()
    flash('You chose a great meal plan for today!', 'success')
    return redirect(url_for('index'))

@app.route('/show-calories', methods=['GET', 'POST'])
@login_required
@account_complete
def show_calories(time_frame=None):
    """ 
    Use the results of the past 1 week for the default visualization, 
    but also show the dropdown form to allow the user to select a different time range. 
    This has values for 1 week, 2 weeks, 3 weeks, and 1 month
    """
    form = CaloriesTimeFilterForm()
    if form.validate_on_submit():
        time_frame = form.time.data
    if time_frame is None:
        calories = UserCaloriesOverTime.query.filter_by(user_id=current_user.id).order_by(UserCaloriesOverTime.id.desc()).limit(7).all()
        time_frame = '1 Week'
    elif time_frame == '1 Week':
        calories = UserCaloriesOverTime.query.filter_by(user_id=current_user.id).order_by(UserCaloriesOverTime.id.desc()).limit(7).all()
    elif time_frame == '2 Weeks':
        calories = UserCaloriesOverTime.query.filter_by(user_id=current_user.id).order_by(UserCaloriesOverTime.id.desc()).limit(14).all()
    elif time_frame == '3 Weeks':
        calories = UserCaloriesOverTime.query.filter_by(user_id=current_user.id).order_by(UserCaloriesOverTime.id.desc()).limit(21).all()
    elif time_frame == '1 Month':
        calories = UserCaloriesOverTime.query.filter_by(user_id=current_user.id).order_by(UserCaloriesOverTime.id.desc()).limit(30).all()

    labels = []
    values = []
    for cl in calories:
        labels.append(cl.created_at.strftime("%m/%d"))
        values.append(cl.calories)

    recommended_intake = UserCalories.query.filter_by(user_id=current_user.id).first().calories
    averaged = round(sum(values) / len(values))

    return render_template('calories_over_time.html', title='Calories Over Time', time_frame=time_frame, labels=labels, values=values, form=form, recommended_intake=recommended_intake, averaged=averaged)



@app.route('/show-bmi/', methods=['GET', 'POST'])
@login_required
@account_complete
def show_bmi(time_frame=None):
    """ 
    Use the results of the past month for the default visualization, 
    but also show the dropdown form to allow the user to select a different time range. 
    This has values for 1 week, 2 weeks, 3 weeks, 1 month, 3 months, 6 months, 1 year.
    """
    form = BMITimeFilterForm()
    if form.validate_on_submit():
        time_frame = form.time.data
    if time_frame is None:
        bmis = UserBMIOverTime.query.filter_by(user_id=current_user.id).filter(UserBMIOverTime.created_at >= datetime.datetime.now() - datetime.timedelta(days=30)).all()
        time_frame = '1 Month'
    elif time_frame == '1 Week':
        bmis = UserBMIOverTime.query.filter_by(user_id=current_user.id).filter(UserBMIOverTime.created_at >= datetime.datetime.now() - datetime.timedelta(days=7)).all()
    elif time_frame == '2 Weeks':
        bmis = UserBMIOverTime.query.filter_by(user_id=current_user.id).filter(UserBMIOverTime.created_at >= datetime.datetime.now() - datetime.timedelta(days=14)).all()
    elif time_frame == '3 Weeks':
        bmis = UserBMIOverTime.query.filter_by(user_id=current_user.id).filter(UserBMIOverTime.created_at >= datetime.datetime.now() - datetime.timedelta(days=21)).all()
    elif time_frame == '1 Month':
        bmis = UserBMIOverTime.query.filter_by(user_id=current_user.id).filter(UserBMIOverTime.created_at >= datetime.datetime.now() - datetime.timedelta(days=30)).all()
    elif time_frame == '3 Months':
        bmis = UserBMIOverTime.query.filter_by(user_id=current_user.id).filter(UserBMIOverTime.created_at >= datetime.datetime.now() - datetime.timedelta(days=90)).all()
    elif time_frame == '6 Months':
        bmis = UserBMIOverTime.query.filter_by(user_id=current_user.id).filter(UserBMIOverTime.created_at >= datetime.datetime.now() - datetime.timedelta(days=180)).all()
    elif time_frame == '1 Year':
        bmis = UserBMIOverTime.query.filter_by(user_id=current_user.id).filter(UserBMIOverTime.created_at >= datetime.datetime.now() - datetime.timedelta(days=365)).all()


    labels = []
    values = []
    for bmi in bmis:
        print(bmi.bmi)
        labels.append(bmi.created_at.strftime("%m/%d"))
        values.append(bmi.bmi)

    return render_template('bmi_over_time.html', title='BMI Over Time', time_frame=time_frame, labels=labels, values=values, form=form)
    


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender = "mealmindy@proton.me", recipients = [user.email])

    msg.body = f"To reset your password, visit the following link : {url_for('reset_token', token=token, _external=True)} If you did not make this request then simply ignore this email and no changes will be made."

    mail.send(msg)

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
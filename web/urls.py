from flask import render_template, request, redirect, url_for, flash
from web import app, db, bcrypt
from web.forms import RegistrationForm, LoginForm, UpdateAccountForm, CalculateCalories
from web.models import User, UserCalories, UserCurrentDiet, UserCurrentDietMeals, Meals, MealsPhotos, MealsLabel, DietCalories
from flask_login import login_user, current_user, logout_user, login_required
from web.meal_planner import choose_meals_for_user
from functools import wraps

def account_complete(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if not (current_user.height and current_user.weight and current_user.age and current_user.goal and current_user.activity_level and current_user.gender):
                flash('Please complete your account details.', 'warning')
                return redirect(url_for('account'))
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
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('index'))
            # flash(f'You have been logged in!', 'success')
        else:
            flash(f'Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.height = form.height.data
        current_user.weight = form.weight.data
        current_user.age = form.age.data
        current_user.goal = form.goal.data
        current_user.activity_level = form.activity_level.data
        current_user.gender = form.gender.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('get_calories'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        if current_user.height: form.height.data = round(current_user.height, 2)
        if current_user.weight: form.weight.data = round(current_user.weight, 2)
        if current_user.age: form.age.data = int(current_user.age)
        if current_user.goal: form.goal.data = current_user.goal
        if current_user.activity_level: form.activity_level.data = current_user.activity_level
        if current_user.gender: form.gender.data = current_user.gender
    return render_template('account.html', title='Account', form=form)


@app.route('/get_calories', methods=['GET'])
@login_required
@account_complete
def get_calories():
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
    user_calories = UserCalories(calories=calories, user_id=current_user.id)
    db.session.add(user_calories)
    db.session.commit()
    return render_template('get_calories.html', title='Get Calories', current_user=current_user, calories=calories)
    
    
@app.route('/get_meals', methods=['GET'])
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

@app.route('/show_meals', methods=['GET'])
@login_required
@account_complete
def show_meals():
    if UserCurrentDiet.query.filter_by(user_id=current_user.id).first():
        print("I am there")
        user_current_diet = UserCurrentDiet.query.filter_by(user_id=current_user.id).first()
        user_current_meals = UserCurrentDietMeals.query.filter_by(user_current_diet_id=user_current_diet.id).all()
        meals = []
        servings = []
        labels=[]
        for user_current_meal in user_current_meals:
            meal = Meals.query.filter_by(id=user_current_meal.meal_id).first()
            meal_id=user_current_meal.meal_id
            print(meal_id)
            label=MealsLabel.query.filter_by(id=meal_id).first()
            meal_type=label.label
            serving_size = user_current_meal.serving_size
            servings.append(serving_size)
            meals.append(meal)
            labels.append(label)
        diet_calories = DietCalories.query.filter_by(user_current_diet_id=user_current_diet.id).first()
        print(diet_calories, meals,labels)
        return render_template('show_meals.html',
                               title='Get Meals',
                               current_user=current_user,
                               meals=meals,
                               diet_calories=diet_calories,
                               servings=servings,
                               labels=labels,
                               zip=zip,
                               round=round)
    else:
        return redirect(url_for('get_meals'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
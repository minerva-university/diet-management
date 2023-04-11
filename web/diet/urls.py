from flask import render_template, request, redirect, url_for, flash
from diet import app, db, bcrypt
from diet.forms import RegistrationForm, LoginForm, UpdateAccountForm, CalculateCalories
from diet.models import User, UserCalories
from flask_login import login_user, current_user, logout_user, login_required


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
                return redirect(url_for('account'))
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
        current_user.gender = form.activity_level.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
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


@app.route('/get_calories', methods=['GET', 'POST'])
def get_calories():
    form = CalculateCalories()
    
    if form.gender.data == 'Male':
        BMR = 66.47 + (13.75 * current_user.weight) + (5.003 * current_user.height) - (6.755 * current_user.age)
    if form.gender.data == 'Female':
        BMR = 655.1 + (9.563 * current_user.weight) + (1.85 * current_user.height) - (4.676 * current_user.age)
    
    if form.activity_level.data == 'Sedentary':
        AMR = BMR * 1.2
    elif form.activity_level.data == 'Lightly Active':
        AMR = BMR * 1.375
    elif form.activity_level.data == 'Moderately Active':
        AMR = BMR * 1.55
    elif form.activity_level.data == 'Very Active':
        AMR = BMR * 1.725
    elif form.activity_level.data == 'Extra Active':
        AMR = BMR * 1.9

    if form.goal.data == 'Lose Weight':
        calories = AMR - 500
    elif form.goal.data == 'Maintain Weight':
        calories = AMR
    elif form.goal.data == 'Gain Weight':
        calories = AMR + 500
    
    user_calories = UserCalories(calories=calories, user_id=current_user.id)
    db.session.add(user_calories)
    db.session.commit()
    return render_template('get_calories.html', title='Get Calories', form=form)
    
    
    


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
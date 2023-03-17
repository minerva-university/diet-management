from flask import render_template, request, redirect, url_for, flash, abort
from diet import app, db, bcrypt
from diet.forms import RegistrationForm, LoginForm, InitializeAccountForm , UpdateAccountForm
from diet.models import User
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
        user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.name.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, legend='Register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            if current_user.height == None or current_user.weight == None or current_user.age == None or current_user.activity_level == None or current_user.specific_diet == None:
                flash('Please initialize your account!', 'info')
                return redirect(url_for('initialize'))
            next_page = request.args.get('next')
            flash(f'You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash(f'Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form, legend='Login')

@app.route('/initialize', methods=['GET', 'POST'])
@login_required
def initialize():
    form = InitializeAccountForm()
    if form.validate_on_submit():
        current_user.height = form.height.data
        current_user.weight = form.weight.data
        current_user.age = form.age.data
        current_user.activity_level = form.activity_level.data
        current_user.specific_diet = form.specific_diet.data
        db.session.commit()
        flash('Your account has been initialized!', 'success')
        return redirect(url_for('index'))
    return render_template('initialize.html', title='Initialize', form=form, legend='Initialize Account')


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.height = form.height.data
        current_user.weight = form.weight.data
        current_user.age = form.age.data
        current_user.activity_level = form.activity_level.data
        current_user.specific_diet = form.specific_diet.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        if current_user.height: form.height.data = round(current_user.height, 2)
        if current_user.weight: form.weight.data = round(current_user.weight, 2)
        if current_user.age: form.age.data = int(current_user.age)
        if current_user.activity_level: form.activity_level.data = current_user.activity_level
        if current_user.specific_diet: form.specific_diet.data = current_user.specific_diet
    return render_template('account.html', title='Account', form=form, legend='Account Information')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/account/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_account(user_id):
    user = User.query.get_or_404(user_id)
    if user != current_user:
        abort(403)

    db.session.delete(user)
    db.session.commit()
    flash('Your account has been deleted!', 'success')
    return redirect(url_for('index'))
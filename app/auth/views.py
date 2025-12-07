from flask import (Blueprint, flash, redirect,
                   render_template, url_for)
from flask_login import login_user, login_required, logout_user
from app.forms import LoginForm, SignUpForm
from app.models import UserData, db, User, UserModel, get_user

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():

    signup_form = SignUpForm()

    context = {
        'signup_form': signup_form
    }

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data

        new_user = User(username=username, password=password)

        # Check if the users exists in the DB
        user_db = get_user(username)

        if user_db:
            # If the user already exists
            flash('User already exists', 'danger')

            return redirect(url_for('auth.signup'))
        else:
            # If does not exists, create it
            db.session.add(new_user)
            db.session.commit()

            # Login the new user
            user_db = get_user(username)
            user_data = UserData(username, password)
            user = UserModel(user_data)
            login_user(user)

            flash('You have successfully signed up!', 'success')

            return redirect(url_for('index'))

    return render_template('signup.html', **context)


@auth.route('/login', methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    context = {
        'login_form': login_form
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        # Check if the user exists in the DB
        user_db = get_user(username)

        if user_db:
            # If the user exists
            user_data = UserData(username, password)
            user = UserModel(user_data)

            # Validate password
            if password == user_db.password:
                login_user(user)

                flash('Succesfully loged in!', 'success')

                return redirect(url_for('index'))
            else:
                # If the passwords does not matchs
                flash('Incorrect password', 'danger')

                return redirect(url_for('auth.login'))
        else:
            # If the user does not exists
            flash('User does not exists', 'danger')

            return redirect(url_for('auth.login'))

    return render_template('login.html', **context)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Succesfully logged out!', 'success')

    return redirect(url_for('index'))

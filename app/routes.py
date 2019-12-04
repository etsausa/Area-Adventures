from datetime import datetime
from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, Location
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post 1'},
        {'author': user, 'body': 'Test post 2'}
    ]
    return  render_template('user.html', user=user, posts=posts)


@app.route('/reset_db')
def reset_db():
    flash("Resetting and populating with Dummy Data")

    # deleting data--
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()

    #dummy data

    u1 = User(username="ADMIN", email="AreaAdventures@gmail.com")
    u1.set_password("Admin1234")
    u2 = User(username="Ethan", email="etsausa@gmail.com")
    u2.set_password("ethaniscool")
    u3 = User(username="Lauren")
    u3.set_password("laurenisalsocool")

    p1 = Post(title="testPost", description="This is a test post. Not much else to it",
              timeStamp=datetime(2019,11,19), is_submitted=True, user_id=1, location_id=2)
    p2 = Post(title="testPost:theSQL", description="This is also a test post but its a little more complicated",
              timeStamp=datetime(1900,1,1), is_submitted=True, user_id=2, location_id=2)

    l1 = Location(Long=-76.489588, Lat=42.435663)
    l2 = Location(Long=0, Lat=0)

    db.session.add(u1)
    db.session.add(u2)
    db.session.add(u3)
    db.session.add(p1)
    db.session.add(p2)
    db.session.add(l1)
    db.session.add(l2)

    db.session.commit()

    return redirect(url_for('index'))

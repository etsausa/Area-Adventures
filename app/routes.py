from datetime import datetime
from app import app, db
from flask import render_template, flash, redirect, url_for, request, jsonify
from app.forms import LoginForm, RegistrationForm, PostForm
from app import app, db, photos
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, PostForm
from app import app, db
from flask import render_template, flash, redirect, url_for, request, jsonify
from app.forms import LoginForm, RegistrationForm, PostForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, PostSchema
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/getPosts', methods=['GET'])
def getPosts():
    posts = Post.query.all()
    post_schema = PostSchema(many=True)
    output = post_schema.dump(posts)

    return jsonify(output)

@app.route('/postLocation', methods=['POST'])
def postLocation():
    print(request.get_json())
    return 'OK' , 200

@app.route("/submit", methods=['GET','POST'])
def submit():
    form = PostForm()
    if form.validate_on_submit():

        p = Post(title=form.loc_name.data, description=form.description.data)

        db.session.add(p)
        db.session.commit()

        flash('Location Submitted')

        return redirect(url_for('index'))

    return render_template('submit.html', form=form)


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

    return render_template('user.html', user=user, posts=posts)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        form = EditProfileForm()
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.about_me = form.about_me.data
            db.session.commit()
            flash('Your changes have been saved.')
            return redirect(url_for('edit_profile'))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.about_me.data = current_user.about_me
        return render_template('edit_profile.html', title='Edit Profile',
                               form=form)


#@app.route('/submit', methods=['GET', 'POST'])
#def upload_file():
#    form = PostForm()
#    if form.validate_on_submit():
#        filename = photos.save(form.photo.data)
#        file_url = photos.url(filename)
#    else:
#        file_url = None
#    return render_template('submit.html', form=form, file_url=file_url)


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
    u1.set_password("1234")
    u2 = User(username="Ethan", email="etsausa@gmail.com")
    u2.set_password("ethaniscool")
    u3 = User(username="Lauren")
    u3.set_password("laurenisalsocool")

    p1 = Post(title="testPost", description="This is a test post. Not much else to it", Long=-76.489588, Lat=42.435663,
              timeStamp=datetime(2019,11,19), is_submitted=True, user_id=1)
    p2 = Post(title="testPost:theSQL", description="This is also a test post but its a little more complicated", Long=0, Lat=0,
              timeStamp=datetime(1900,1,1), is_submitted=True, user_id=2)

    db.session.add(u1)
    db.session.add(u2)
    db.session.add(u3)
    db.session.add(p1)
    db.session.add(p2)

    db.session.commit()

    return redirect(url_for('index'))

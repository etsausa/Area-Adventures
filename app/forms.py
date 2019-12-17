import os
from flask_wtf import FlaskForm, validators
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, DecimalField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app.models import User
from app import photos
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
#------------------- Login Form------------------------#
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

#------------------- Registration Form------------------------#
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    #Uncomment when database is implemented

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user is not None:
            raise ValidationError('Please use a different email address.')

#------------------- Post Form------------------------#
class PostForm(FlaskForm):
    longitude = DecimalField('Longitude', validators=[DataRequired()])
    latitude = DecimalField('Latitude', validators=[DataRequired()])
    loc_name = StringField('Location Title', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Submit Post')

    # image = FileField(u'Image',[validators.regexp(u'^[^/\\]\.jpg$')]) )
    #
    # def validate_image(form, field):
    #     if field.data:
    #         field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)
    # def upload(request):
    #     form = PostForm(request.post)
    #     if form.image.data:
    #         image_data = request.FILES[form.image.name].read()
    #     open(os.path.join(".", form.image.data), 'w').write(image_data)
    # destName = StringField('Name', validators=[DataRequired()])
    # field_latitude = FloatField(u'Latitude', default=-30, validators=[DataRequired()], description='48.182601')
    # field_longitude = FloatField(u'Longitude', default=150, validators=[DataRequired()], description='11.304939')
    # description = StringField('Description', validators=[DataRequired()])

    # loc_name = StringField('Location Title', validators=[DataRequired()])
    # longitude = DecimalField('Longitude', validators=[DataRequired()])
    # latitude = DecimalField('Latitude', validators=[DataRequired()])
    # description = StringField('Description')

    #photo = FileField(validators=[FileAllowed(photos, 'Image only!'), FileRequired('File was empty!')])

    #submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')


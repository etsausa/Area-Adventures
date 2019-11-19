from flask_wtf import FlaskForm, validators
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, FileField, MultipleFileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

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
    loc_name = StringField('Username', validators=[DataRequired()])
    longitude = DecimalField('Longitude', validators=[DataRequired()])
    Latitude = DecimalField('Latitude', validators=[DataRequired()])
    description = StringField('Description')
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

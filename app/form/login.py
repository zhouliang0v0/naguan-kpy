from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(Form):
    email = StringField('email', validators=[DataRequired('accountNumber is null')])
    password = PasswordField('password', validators=[DataRequired('password is null')])
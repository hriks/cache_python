from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms import SelectField


class RegisterForm(Form):
    role = SelectField(
        'Account Type', choices=[
            ('admin', 'Admin'),
            ('manager', 'Manager'),
            ('user', 'User')])

    userid = TextField(
        'Username', validators=[DataRequired(), Length(min=2, max=25)]
    )

    name = TextField(
        'Name', validators=[DataRequired(), Length(min=6, max=25)]
    )

    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )

    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=2, max=40)]
    )


class LoginForm(Form):
    name = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class PostMessage(Form):
    message = TextField('Message', [DataRequired()])


class UpdateForm(Form):
    role = SelectField(
        'Account Type', choices=[
            ('admin', 'Admin'),
            ('manager', 'Manager'),
            ('user', 'User')])

    userid = TextField(
        'New Username', validators=[DataRequired(), Length(min=2, max=25)]
    )

    name = TextField(
        'New Name', validators=[Length(min=6, max=25)]
    )

    email = TextField(
        'New Email', validators=[Length(min=6, max=40)]
    )

    password = PasswordField(
        'New Password', validators=[Length(min=2, max=40)]
    )

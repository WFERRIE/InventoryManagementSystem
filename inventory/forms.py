from flask_wtf import FlaskForm
from werkzeug.routing import ValidationError
from wtforms import StringField, SubmitField, DecimalField, IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from inventory.models import Item

# class RegistrationForm(FlaskForm):
#     def validate_username(self, username_to_check):
#         user = User.query.filter_by(username = username_to_check.data).first()
#         if user:
#             raise ValidationError('Username already exists.')

#     def validate_email_address(self, email_address_to_check):
#         email_address = User.query.filter_by(email_address = email_address_to_check.data).first()
#         if email_address:
#             raise ValidationError('Email already has account associated with it.')

#     username = StringField(label = 'Username', validators = [Length(min=2, max=30), DataRequired()])
#     email_address = StringField(label = 'Email Address', validators = [Email(), DataRequired()])
#     password1 = PasswordField(label = 'Password', validators = [Length(min=6, max = 100), DataRequired()])
#     password2 = PasswordField(label = 'Confirm Password', validators = [EqualTo('password1'), DataRequired()])
#     submit = SubmitField(label = 'Create Account')

# class LoginForm(FlaskForm):
#     username = StringField(label= "Username", validators=[DataRequired()])
#     password = PasswordField(label= "Password", validators=[DataRequired()])
#     submit = SubmitField(label = 'Sign in')

class AddItemForm(FlaskForm):
    submit = SubmitField(label="Create Item")    

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label="Purchase Item")

class CreateItemForm(FlaskForm):
    name = StringField(label = 'Name', validators = [Length(min=2, max=30), DataRequired()])
    price = DecimalField(places = 2, validators = [DataRequired()])
    quantity = DecimalField(validators = [DataRequired()])
    barcode = IntegerField(validators = [DataRequired()])
    description = StringField(label = 'Name', validators = [Length(min=2, max=1024), DataRequired()])
    submit = SubmitField(label="Create Item")
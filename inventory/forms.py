from flask_wtf import FlaskForm
from werkzeug.routing import ValidationError
from wtforms import StringField, SubmitField, DecimalField, IntegerField
from wtforms.validators import Length, DataRequired, ValidationError, NumberRange
from inventory.models import Item

class CreateItemForm(FlaskForm):
    name = StringField(label = 'Name', validators = [Length(min=2, max=30), DataRequired()])
    price = DecimalField(label = 'Price', validators = [DataRequired()])
    quantity = IntegerField(label = 'Quantity', validators = [DataRequired()])
    barcode = IntegerField(label = 'Barcode', validators = [NumberRange(min = 0, max = 999999999999), DataRequired()])
    description = StringField(label = 'Description', validators = [Length(min=2, max=1024), DataRequired()])
    submitCreating = SubmitField(label = "Create Item")


class DeleteItemForm(FlaskForm):
    submitDeleting = SubmitField(label = "Delete Item")


class EditItemForm(CreateItemForm):
    submitEditing = SubmitField(label = "Save Changes")
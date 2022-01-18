from flask_wtf import FlaskForm
from werkzeug.routing import ValidationError
from wtforms import StringField, SubmitField, DecimalField, IntegerField
from wtforms.validators import Length, DataRequired, ValidationError
from inventory.models import Item

class CreateItemForm(FlaskForm):
    name = StringField(label = 'Name', validators = [Length(min=2, max=30), DataRequired()])
    price = DecimalField(label = 'Price', validators = [DataRequired()])
    quantity = IntegerField(label = 'Quantity', validators = [DataRequired()])
    barcode = StringField(label = 'Barcode', validators = [DataRequired()])
    description = StringField(label = 'Description', validators = [Length(min=2, max=1024), DataRequired()])
    submitCreating = SubmitField(label = "Create Item")
    
    def validate_unique(self, parameter, value):
        if Item.query.filter_by(parameter = value).first():
            raise ValidationError(f"{parameter} must be Unique.")


class DeleteItemForm(FlaskForm):
    submitDeleting = SubmitField(label = "Delete Item")


class EditItemForm(FlaskForm):
    name = StringField(label = 'Name', validators = [Length(min=2, max=30), DataRequired()])
    price = StringField(label = 'Price', validators = [DataRequired()])
    quantity = StringField(label = 'Quantity', validators = [DataRequired()])
    barcode = StringField(label = 'Barcode', validators = [DataRequired()])
    description = StringField(label = 'Description', validators = [Length(min=2, max=1024), DataRequired()])
    submitEditing = SubmitField(label = "Save Changes")
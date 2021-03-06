from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import Length, DataRequired, Regexp

class CreateItemForm(FlaskForm):
    name = StringField(label = 'Name', validators = [Length(min=2, max=30), DataRequired()])
    price = DecimalField(label = 'Price', validators = [DataRequired()])
    quantity = DecimalField(label = 'Quantity', validators = [DataRequired()])
    barcode = StringField(label = '12 Digit UPC Barcode', validators = [Regexp('^(\d{12})$', message = "Invalid UPC Barcode. Please ensure barcode is 12 digits."), DataRequired()])
    description = StringField(label = 'Description', validators = [Length(min=2, max=1024), DataRequired()])
    submitCreating = SubmitField(label = "Create Item")


class DeleteItemForm(FlaskForm):
    submitDeleting = SubmitField(label = "Delete Item")


class EditItemForm(CreateItemForm):
    submitEditing = SubmitField(label = "Save Changes")
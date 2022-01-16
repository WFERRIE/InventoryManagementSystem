from inventory import app
from flask import render_template, redirect, url_for, flash, request
from inventory.models import Item
from inventory.forms import DeleteItemForm, CreateItemForm
from inventory import db

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/inventory', methods=['GET', 'POST'])
def inventory_page():
    deleting_form = DeleteItemForm()
    creating_form = CreateItemForm()
    if request.method == "POST":

        if creating_form.validate_on_submit():
            print(f'Name: {creating_form.name.data}, price: {creating_form.price.data}, quantity: {creating_form.quantity.data} ,barcode: {creating_form.barcode.data} , description: {creating_form.description.data},')
            item_to_create = Item(name = creating_form.name.data, price = creating_form.price.data, quantity = creating_form.quantity.data, barcode = creating_form.barcode.data, description = creating_form.description.data)
            db.session.add(item_to_create)
            db.session.commit()
            flash(f'Item created successfully! {item_to_create.name} has been added to the Inventory.', category='success')

            return redirect(url_for('inventory_page'))

        # if creating_form.errors != {}:
        #     for err_msg in creating_form.errors.values():
        #         flash(f'There was an error creating an item: {err_msg}', category='danger')
        
        if deleting_form.validate_on_submit():
            deleting_item_id = request.form.get('deleting_item_id')
            deleting_item_name = request.form.get('deleting_item_name')
            Item.query.filter_by(id=deleting_item_id).delete()
            db.session.commit()
            flash(f"Successfully deleted {deleting_item_name} from the Inventory.", category='success')
            return redirect(url_for('inventory_page'))

        # created_item = request.form.get('created_item')
        # c_item_obj = Item.query.filter_by(name = created_item).first()
        # if c_item_obj:
        #     c_item_obj.createItem()
        #     flash(f"Item has been created and added to Inventory.")

        return redirect(url_for('inventory_page'))

    if request.method == "GET":
        items = Item.query.all()
        return render_template('inventory.html', items=items, deleting_form = deleting_form, creating_form = creating_form)
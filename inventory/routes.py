from inventory import app
from flask import render_template, redirect, url_for, flash, request
from inventory.models import Item
from inventory.forms import PurchaseItemForm, CreateItemForm
from inventory import db

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/inventory', methods=['GET', 'POST'])
def inventory_page():
    purchase_form = PurchaseItemForm()
    creating_form = CreateItemForm()
    if request.method == "POST":

        if creating_form.validate_on_submit():
            item_to_create = Item(name = creating_form.name.data, price = creating_form.price.data, quantity = creating_form.quantity.data, barcode = creating_form.barcode.data, description = creating_form.description.data)
            db.session.add(item_to_create)
            db.session.commit()
            flash(f'Item created successfully! {item_to_create.name} has been added to the Inventory.', category='success')

            return redirect(url_for('market_page'))

        if creating_form.errors != {}:
            for err_msg in creating_form.errors.values():
                flash(f'There was an error creating an item: {err_msg}', category='danger')

        # created_item = request.form.get('created_item')
        # c_item_obj = Item.query.filter_by(name = created_item).first()
        # if c_item_obj:
        #     c_item_obj.createItem()
        #     flash(f"Item has been created and added to Inventory.")

        return redirect(url_for('inventory_page'))

    if request.method == "GET":
        items = Item.query.all()
        return render_template('inventory.html', items=items, purchase_form = purchase_form, creating_form = creating_form)



@app.route('/register', methods = ['GET', 'POST'])
def registration_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_to_create = User(username = form.username.data, email_address = form.email_address.data, password = form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully. Welcome {user_to_create.username}!', category='success')


        return redirect(url_for('market_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error creating a user: {err_msg}', category='danger')

    return render_template('register.html', form = form)
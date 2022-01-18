from inventory import app
from flask import render_template, redirect, url_for, flash, request, send_file
from inventory.models import Item
from inventory.forms import DeleteItemForm, CreateItemForm, EditItemForm
from inventory import db
import sqlite3
import csv

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/inventory', methods=['GET', 'POST'])
def inventory_page():
    deleting_form = DeleteItemForm()
    creating_form = CreateItemForm()
    editing_form = EditItemForm()
    items_displayed_per_page = 10

    if request.method == "POST":
        if creating_form.submitCreating.data and creating_form.validate(): #check that we're submitting the create item form
            if creating_form.validate_on_submit(): #check that the form submission is valid
                non_unique_barcode = Item.query.filter_by(barcode = creating_form.barcode.data).first()

                if non_unique_barcode: #check uniqueness of barcode
                    flash(f"Error: The barcode '{creating_form.barcode.data} already exists in this database as '{non_unique_barcode.name}' with database ID: '{non_unique_barcode.id}'. Please enter a unique barcode when creating a new item.", category = "danger")
                    return redirect(url_for('inventory_page'))

                else:
                    item_to_create = Item(name = creating_form.name.data, price = creating_form.price.data, quantity = creating_form.quantity.data, barcode = creating_form.barcode.data, description = creating_form.description.data)
                    db.session.add(item_to_create)
                    try:
                        db.session.commit()
                    except:
                        flash(f"Something went wrong trying to create the item. Please refresh and try again.", category = 'danger')

                    flash(f'Item created successfully! {item_to_create.name} has been added to the Inventory.', category='success')

                    return redirect(url_for('inventory_page'))

            elif creating_form.errors != {}:
                for err_msg in creating_form.errors.values():
                    flash(f'There was an error creating an item: {err_msg}', category='danger')

            return redirect(url_for('inventory_page'))
        

        elif deleting_form.submitDeleting.data and deleting_form.validate():
            if deleting_form.validate_on_submit():
                deleting_item_id = request.form.get('deleting_item_id')
                deleting_item_name = request.form.get('deleting_item_name')
                Item.query.filter_by(id=deleting_item_id).delete()
                try:
                    db.session.commit()
                except:
                    flash(f"Something went wrong trying to delete the item. Please refresh and try again.", category = 'danger')

                flash(f"Successfully deleted {deleting_item_name} from the Inventory.", category='success')
                return redirect(url_for('inventory_page'))

        elif editing_form.submitEditing.data and editing_form.validate():            
            if editing_form.validate_on_submit():
                editing_item_id = request.form.get('editing_item_id')
                non_unique_barcode = Item.query.filter_by(barcode = editing_form.barcode.data).first()

                if non_unique_barcode and (int(non_unique_barcode.id) != int(editing_item_id)): #check uniqueness of barcode
                    flash(f"Error: The barcode '{editing_form.barcode.data} already exists in this database as '{non_unique_barcode.name}' with database ID: '{non_unique_barcode.id}'. Please enter a unique barcode when creating a new item.", category = "danger")
                    return redirect(url_for('inventory_page'))
                
                else:
                    editing_item_id = request.form.get('editing_item_id')
                    item_to_edit = Item.query.filter_by(id = editing_item_id).first()
                    
                    item_to_edit.name = editing_form.name.data
                    item_to_edit.price = editing_form.price.data
                    item_to_edit.quantity = editing_form.quantity.data
                    item_to_edit.barcode = editing_form.barcode.data
                    item_to_edit.description = editing_form.description.data

                    try:
                        db.session.commit()
                        return redirect(url_for('inventory_page'))
                    except:
                        flash(f"Something went wrong trying to edit the item. Please refresh and try again.", category = 'danger')

        return redirect(url_for('inventory_page'))

    if request.method == "GET":
        page = request.args.get('page', 1, type = int)
        items = Item.query.paginate(page = page, per_page = items_displayed_per_page)
        return render_template('inventory.html', items=items, deleting_form = deleting_form, creating_form = creating_form, editing_form = editing_form)


@app.route('/export')
def export_page():
    con = sqlite3.connect('inventory/inventory.db')
    outfile = open('export.csv', 'w', newline = '')
    outcsv = csv.writer(outfile)

    cursor = con.execute('select * from item')

    # outcsv.writerow(x[0] for x in cursor.description)
    outcsv.writerows(cursor.fetchall())

    outfile.close()
    con.close()
    return send_file('../export.csv', as_attachment = True, attachment_filename = 'export.csv', mimetype = "text/csv")



@app.route('/error')
def error_page():
    return render_template('error.html')

@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('error_page'))
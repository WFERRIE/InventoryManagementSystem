from inventory import db
from flask import send_file
import sqlite3
import csv




def exportFile():
    con = sqlite3.connect('inventory/inventory.db')
    outfile = open('export.csv', 'w', newline = '')
    outcsv = csv.writer(outfile)

    cursor = con.execute('select * from item')

    # outcsv.writerow(x[0] for x in cursor.description)
    outcsv.writerows(cursor.fetchall())

    outfile.close()
    con.close()
    return send_file('../export.csv', as_attachment = True, attachment_filename = 'export.csv', mimetype = "text/csv")

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(length = 30), nullable = False)
    price = db.Column(db.Float(), nullable = False)
    quantity = db.Column(db.Float(), nullable = False)
    barcode = db.Column(db.String(length = 12), nullable = False, unique = True)
    description = db.Column(db.String(length = 1024), nullable = False)


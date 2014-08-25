#views.py

#################
#### imports ####
#################
from flask import Flask, flash, redirect, render_template, session, url_for, request, make_response
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from functools import wraps
from flask_wtf import Form
from wtforms import TextAreaField, IntegerField
from wtforms.validators import DataRequired
import random



import pdb

################
#### config ####
################

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

################
#### models ####
################

class Item(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    mrn = db.Column(db.String, nullable=False)
    patientNotes = db.Column(db.String, nullable=True)
    attending = db.Column(db.String, nullable=True)
    ward = db.Column(db.String, nullable=True)

    def __init__(self, firstname, mrn, patientNotes, attending, ward):
        self.firstname = firstname
        self.mrn = mrn
        self.patientNotes = patientNotes
        self.attending = attending
        self.ward = ward


################
#### forms  ####
################

class ImportData(Form):
    data_Id = IntegerField('Your Data ID is', default="", validators=[DataRequired()])
    patientData = TextAreaField('Patient data', default="", validators=[DataRequired()])

#################
#### methods ####
#################

#class ParseData(something):
#    pass


################
#### routes ####
################

@app.route('/', methods=['GET', 'POST'])
def data():
    error = None
    form = ImportData(request.form)
    form.data_Id.data = random.randint(1000, 9999)
    if request.method == 'POST':
        if form.validate_on_submit():
            ImportedData = form.patientData.data
            print ImportedData
            flash('data imported. Now use your app')
            return render_template("home.html", form=form)
        else:
            return render_template("home.html", form=form, error=error)
    if request.method == 'GET':
        return render_template("home.html", form=form, data_Id=random.randint(1000, 9999))















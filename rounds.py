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
from flask.ext.restful import Resource, Api, reqparse, fields, marshal_with, marshal
import random



import pdb

################
#### config ####
################

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
api = Api(app)

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
    bed = db.Column(db.String, nullable=True)
    data_id = db.Column(db.Integer, nullable=False)

    def __init__(self, firstname, mrn, patientNotes, attending, ward, bed, data_id):
        self.firstname = firstname
        self.mrn = mrn
        self.patientNotes = patientNotes
        self.attending = attending
        self.ward = ward
        self.bed = bed
        self.data_id = data_id


################
#### forms  ####
################

class ImportData(Form):
    data_Id = IntegerField('Your Data ID is', default=random.randint(1000, 9999), validators=[DataRequired()])
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
    if request.method == 'POST':
        #pdb.set_trace()
        if form.validate_on_submit():
            from StringIO import StringIO
            inputIO = StringIO(form.patientData.data)
            import csv
            for line in csv.reader(inputIO, delimiter='\t'):
                if len(line) < 2:
                    continue
                #
                # in here I need to create a method to filter out a row that has a shitty 
                #  number of tabs or an extra return.
                # wardsplit = (((line[3][:-10]).partition(' ')[0])[0]) + (line[3][:-10]).partition(' ')[2]
                # wardsplit = (((x[:-10]).partition(' ')[0])[0]) + (x[:-10]).partition(' ')[2]
                data_identifier = random.randint(1000, 9999)
                namesplit = line[2].partition(',')[0]
                surnamesplit = line[5].partition(',')[0]
                bedsplit = line[3][-5:]
                wardsplit = (((line[3][:-10]).partition(' ')[0])[0]) + (line[3][:-10]).partition(' ')[2]
                # patient structure = (firstname, mrn, patientNotes, attending, ward, bed, data_id):
                new_patient = Item(namesplit, line[4], line[10], surnamesplit, wardsplit, bedsplit, form.data_Id.data)
                db.session.add(new_patient)
                db.session.commit()
            flash('data imported. Now use your app to import')
            return render_template("home.html", form=form, data_Id = form.data_Id.data)
        else:
            return render_template("home.html", form=form, error=error)
    if request.method == 'GET':
        return render_template("home.html", form=form, data_Id = form.data_Id.data)



################
#### apis   ####
################

patient_fields = {
    'item_id' : fields.Integer,
    'firstname' : fields.String,
    'mrn' : fields.String,
    'patientNotes' : fields.String,
    'attending' : fields.String,
    'ward' : fields.String,
    'bed' : fields.String,
}

class PatientsAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('item_id', type = int, location = 'json') #help = 'No Task ID provided',
        self.reqparse.add_argument('firstname', type = str, default = "", location = 'json')
        self.reqparse.add_argument('mrn', type = str, default = "", location = 'json')
        self.reqparse.add_argument('patientNotes', type = str, default = "", location = 'json')
        self.reqparse.add_argument('attending', type = str, default = "", location = 'json')
        self.reqparse.add_argument('ward', type = str, default = "", location = 'json')
        self.reqparse.add_argument('bed', type = str, default = "", location = 'json')
        super(PatientsAPI, self).__init__()

    @marshal_with(patient_fields)
    def get(self, data_id):
        results = db.session.query(Item).filter_by(data_id=data_id).all()
        db.session.query(Item).filter_by(data_id=data_id).delete()
        db.session.commit()
        return results

        # curl -i -H "Content-Type: application/json" -X GET http://localhost:5000/api/v1.0/patients/2915

class AllPatientsAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('item_id', type = int, location = 'json') #help = 'No Task ID provided',
        self.reqparse.add_argument('firstname', type = str, default = "", location = 'json')
        self.reqparse.add_argument('mrn', type = str, default = "", location = 'json')
        self.reqparse.add_argument('patientNotes', type = str, default = "", location = 'json')
        self.reqparse.add_argument('attending', type = str, default = "", location = 'json')
        self.reqparse.add_argument('ward', type = str, default = "", location = 'json')
        self.reqparse.add_argument('bed', type = str, default = "", location = 'json')
        super(AllPatientsAPI, self).__init__()

    @marshal_with(patient_fields)
    def get(self):
        results = db.session.query(Item).all()
        #db.session.query(Item).filter_by(data_id=data_id).delete()
        #db.session.commit()
        return results

api.add_resource(PatientsAPI, '/api/v1.0/patients/<int:data_id>', endpoint='patientsAPI')
api.add_resource(AllPatientsAPI, '/api/v1.0/patients/', endpoint='AllPatients') #curl -i http://localhost:5000/api/v1.0/items







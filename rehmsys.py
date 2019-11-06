from flask import Flask, request,json, jsonify # flask main flamework, json files
from flask_sqlalchemy import SQLAlchemy #ease sqlcommands
from flask_marshmallow import Marshmallow
import os

#Initilizing the app
app = Flask(__name__)

#Setting up the sqlalchemy database uri, it willt be in our 
# root but the server needs to know
basedir = os.path.abspath(os.path.dirname(__file__))
    
#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #avoid warning in console

#intialize sqlalchemy
db = SQLAlchemy(app)
#intialize marshmallow
ma = Marshmallow(app)


#basic route
'''
@app.route('/',methods=['GET'])
def get():
    return jsonify({"Hello":"I am Josh"})
'''

#login/signup class/model
class Signup(db.Model):
    id = db.Column(db.Integer,unique = True)
    username = db.Column(db.String(100),primary_key = True,unique=True)#different usernames
    password = db.Column(db.String(255))
    temperature = db.Column(db.String(10))
    heartRate = db.Column(db.String(10))

    #constructor/initializer
    def __init__(self,username,password,temperature,heartRate):
        #adding them to the instances
        self.username = username
        self.password = password
        self.temperature = temperature
        self.heartRate = heartRate

#Signup schema
class signupSchema(ma.Schema):
    class Meta:#items to be shown
        fields = ('id','username','password','temperature','heartRate')

#initializing the signup schema
signup_schema = signupSchema()#to avoid warmings strict= True
patients_schema = signupSchema(many=True)#returning patients

#creating the database
#--python
#from rehmsys import db
#db.create_all()

#interacting with the database using routes
#signing a new person
@app.route('/Signup',methods = ['POST'])
def add_patient():
    username = request.json['username']
    password = request.json['password']
    temperature = request.json['temperature']
    heartRate = request.json['heartRate']

    new_patient = Signup(username,password,temperature,heartRate)

    #adding to the bd
    db.session.add(new_patient)
    db.session.commit()
    
    return signup_schema.jsonify(new_patient)   #want to see what i just created

#return all patients
@app.route('/Signup',methods = ['GET'])
def get_patients():
    all_patients = Signup.query.all()#return all patients
    result = patients_schema.dump(all_patients)
    return jsonify(result)   #return a list of patients

#search a patient
#passing a an int @app.route('/Signup/<id>',methods=['GET'] )///for primary key
@app.route('/Signup/<userName>',methods = ['GET'])#user name as primary key
def get_patient(userName):
    result = {}
    patient_username = Signup.query.get(userName)#return patient username
    result = signup_schema.jsonify(patient_username)
    return result #returns patient username and password

#update a patient's vitals
@app.route('/Signup/<userName>',methods = ['PUT'])
def update_patient(userName):
    patient = Signup.query.get(userName)

    #items to be updated
    temperature = request.json['temperature']
    heartRate = request.json['heartRate']

    updated_temperature = str(patient.temperature) +","+ str(temperature)
    updated_heartRate = str(patient.heartRate) +","+ str(heartRate)

    patient.temperature = updated_temperature
    patient.heartRate = updated_heartRate

    print(updated_temperature)
    print(updated_temperature)
    #adding to the bd
    db.session.commit()
    return signup_schema.jsonify(patient)   #want to see what i just created

#Delete a patient
@app.route('/Signup/<userName>',methods = ['DELETE'])#user name as primary key
def delete_patient(userName):
    patient = Signup.query.get(userName)
    db.session.delete(patient)
    db.session.commit()
    return signup_schema.jsonify(patient) #returns patient username and password

#run server
#checking if main file is equal to main
if __name__=='__main__':
    app.run(debug=True) #callig the app object to run under debug

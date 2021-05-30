# Name:  Jasmeet Singh
# Student Id : 

import flask
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String , Float
import os
from flask_marshmallow import Marshmallow
from flask_pymongo import PyMongo
from flask import Flask, render_template, url_for, request, session, redirect
import bcrypt
from pymongo import MongoClient

# flask application object
app = flask.Flask(__name__)

app.config["DEBUG"] = True

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'app1.db')

db = SQLAlchemy(app)
ma = Marshmallow(app)


@app.route('/mcit/cst-students/all',methods=['GET'])
def student_all():
    student_list = Student1.query.all()
    result =  student_schema.dump(student_list)
    return jsonify(result)

@app.route('/mcit/cst-students/<int:id>',methods=['GET'])
def student_id(id):

    results = []

    student_list = Student1.query.all()
    student_list = student_schema.dump(student_list)
    for student in student_list:
        if student['ID'] == id:
            results.append(student)
            return jsonify(results)


    if not results:
        return "Error : Id not found"
    else:       
        return jsonify(results)



class Student1(db.Model):
    __tablename__ = 'students'
    ID = Column(Integer ,primary_key=True)
    Name = Column(String)
    Branch = Column(String)
    College = Column(String)
    Batch = Column(String)
    Program = Column(String)
    Course =  Column(String)
    First_Language = Column(String)


class StudentSchema1(ma.Schema):
    class Meta:
        fields = ('ID','Name','Branch','College','Batch','Program','Course','First_Language')



student_schema = StudentSchema1()
student_schema = StudentSchema1(many=True)


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created')
    
@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Databse Dropped')

@app.cli.command('db_seed')
def db_seed():
    Jasmeet = Student1(Name = 'Jasmeet Singh',
                      Branch = 'CS',
                      College = 'MCIT',
                      Batch = 'A',
                      Program = 'CST',
                      Course = 'Advance Programming',
                      First_Language = 'Java')
    Manpreet = Student1(Name = 'Manpreet Singh',
                      Branch = 'CS',
                      College = 'MCIT',
                      Batch = 'A',
                      Program = 'CST',
                      Course = 'Advance Programming',
                      First_Language = 'C')      


    db.session.add(Jasmeet)
    db.session.add(Manpreet)
      
    db.session.commit()
    print('Database seeded')


app.config["MONGO_URI"] = "mongodb+srv://cst_user:mcit123@cluster0.vo3fn.mongodb.net/jasmeet?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
mongo_client = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo_client.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo_client.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')

app.run()
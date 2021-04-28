from flask import Flask, render_template, request, session, redirect
import json
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)

class Users(db.Model):
	sno = db.Column(db.Integer, primary_key=True)
	fname = db.Column(db.String(80),nullable=False)
	lname = db.Column(db.String(80),nullable=False)
	email = db.Column(db.String(100), nullable=False)
	password = db.Column(db.String(100), nullable=False)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80), nullable=False)
    lname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200),nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    city = db.Column(db.String(20),nullable=False)
    state = db.Column(db.String(50),nullable=False)
    zipcode = db.Column(db.String(20),nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    
@app.route('/')
def index():
	if ('user_email' in session and 'user_password' in session):
		return render_template('index.html',params=params)
	else:
		return redirect('/login')

@app.route('/login')
def login():
	if ('user_email' in session and 'user_password' in session):
		return redirect('/')
	return render_template('ulogin.html',params=params)

@app.route('/logout')
def logout():
	session.pop('user_email')
	session.pop('user_password')
	return redirect('/')

@app.route('/register',methods=['POST','GET'])
def register():
	if request.method == 'POST':
		fname = request.form.get('fname')
		lname = request.form.get('lname')
		email = request.form.get('email')
		password = request.form.get('password')
		entry = Users(fname=fname,lname=lname,email=email.lower(),password=password)
		db.session.add(entry)
		db.session.commit()
		session['user_email'] = email
		session['user_password'] = password
		return redirect('/')
	return render_template('register.html',params=params)

@app.route('/validation',methods=['POST'])
def validate():
	try:
		email = request.form.get('uemail')
		password = request.form.get('upassword')
		users = Users.query.filter_by(email=email).first()
		if (str(users.email) == email.lower() and str(users.password) == password):
			session['user_email'] = email
			session['user_password'] = password
			return redirect('/')
	except:
		return redirect('/login')

@app.route('/contacts',methods=['GET','POST'])
def contact():
	if ('user_email' in session and 'user_password' in session):
		if request.method=='POST':
			fname = request.form.get('fname')
			lname = request.form.get('lname')
			email = request.form.get('email')
			address = request.form.get('address')
			city = request.form.get('city')
			state = request.form.get('state')
			zipcode = request.form.get('zipcode')
			msg = request.form.get('msg')
			phone_num = request.form.get('phone_num')
			entry = Contacts(date=datetime.now(),fname=fname,lname=lname,email=email,address=address,city=city,state=state,zipcode=zipcode,msg=msg,phone_num=phone_num)
			db.session.add(entry)
			db.session.commit()
			return redirect('/')
		return render_template('contact.html',params=params)
	return redirect('/')

if __name__ =='__main__':
    app.run(debug=True)

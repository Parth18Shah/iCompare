from flask import render_template,redirect ,url_for ,flash
from icomp.forms import SignUpForm,LoginForm
from icomp.models import User ,News
from icomp import app ,db ,bcrypt
from flask_login import login_user ,current_user ,logout_user

@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html')

@app.route("/about")
def about():
	return render_template('about.html')

@app.route("/products")
def products():
	return render_template('products.html')

@app.route("/contact")
def contact():
	return render_template('contact.html')

@app.route("/login" ,methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		redirect(url_for('home'))
	form=LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password,form.password.data):
			login_user(user,remember=form.remember.data)
			flash('You are successfully logged in!', 'success')
			return redirect(url_for('home'))
		else:
			flash('Check your email and password!')
	return render_template('login.html',form=form)


@app.route("/signup",methods=['GET','POST'])
def signup():
	if current_user.is_authenticated:
		redirect(url_for('home'))
	form = SignUpForm()
	if form.validate_on_submit():
		hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data,email=form.email.data,password=hashed_pass)
		db.session.add(user)
		db.session.commit()
		flash(f'Account created successfully for  { form.username.data }' ,'success')
		return redirect(url_for('login'))
	return render_template('signup.html',form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))
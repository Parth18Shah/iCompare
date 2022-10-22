from flask import render_template,redirect ,url_for ,flash, request, send_file,session
from icomp.forms import SignUpForm,LoginForm
from icomp.models import User ,News
from icomp import app ,db ,bcrypt
from flask_login import login_user ,current_user ,logout_user, login_required
import numpy as np
import pickle
import warnings
from icomp.flipkart_scrapper import flipkart_scraping
from icomp.amazon_scrapper import amazon_scrapping
from icomp.news_scrapper import news_scrapping
warnings.filterwarnings("ignore")


n1_title=''
n1_link=''
n1_content=''
n2_title=''
n2_link=''
n2_content=''
n3_title=''
n3_link=''
n3_content=''


@app.route("/")
@app.route("/home",methods=['GET','POST'])
def home():
	global n1_title,n2_title,n3_title,n1_link,n2_link,n3_link,n1_content,n2_content,n3_content
	if n1_title=='' or n2_title=='' or n3_title=='' or n1_link=='' or n2_link=='' or n3_link=='' or n1_content=='' or n2_content=='' or n3_content=='':
		news_data = news_scrapping()
		n1_title = news_data['title'][0].strip()
		n2_title = news_data['title'][1].strip()
		n3_title = news_data['title'][2].strip()
		n1_link = news_data['link'][0]
		n2_link = news_data['link'][1]
		n3_link = news_data['link'][2]
		n1_content = news_data['content'][0]
		n2_content = news_data['content'][1]
		n3_content = news_data['content'][2]
	return render_template('home_final.html',n1_title=n1_title,n1_link=n1_link,n2_link=n2_link,n3_link=n3_link,n2_title=n2_title,n3_title=n3_title,n1_content=n1_content,n2_content=n2_content,n3_content=n3_content)

@app.route("/about")
def about():
	return render_template('about_final.html')

@app.route("/products",methods=['GET','POST'])
@login_required
def products():
	pred=None
	if request.method == "POST":
		product_name = request.form["product"]
		print("hii" + product_name)
		return redirect(url_for("product",p_name=product_name))
	else:
		# global name ,price, description, a_name, a_price, a_description
		# name = request.args.get('product')
		# if(name):
		# 	flip_data = flipkart_scraping(name)
		# 	if(flip_data):
		# 		name = flip_data["name"]
		# 		price = flip_data["price"]
		# 		description = flip_data["description"]
		# 	else:
		# 		pass
		# 		name = "Not found"
		# 	amazon_data = amazon_scrapping(name)
		# 	if (amazon_data):
		# 		a_name = amazon_data["name"]
		# 		a_price = amazon_data["price"]
		# 		a_description = amazon_data["description"]
		# 	else:
		# 		pass
		# 		a_name = "Not found"
		# 	return render_template('products_final.html',flip_name = name,flip_price=price,flip_des=description ,amazon_name = a_name,amazon_price=a_price,amazon_des=a_description ,pred=pred)
		# else:
		# 	return render_template('products_final.html',pred=pred)
		return render_template('products_final.html',pred=pred)
	

@app.route('/newroute',methods=['GET','POST'])
def newroute():
	if request.method == 'GET':
		pro = request.form['iphone7']
		print("Sdsdsf  =  ",pro)

@app.route("/<p_name>")
def product(p_name):
	flip_data = flipkart_scraping(p_name)
	if(flip_data):
		name = flip_data["name"]
		price = flip_data["price"]
		description = flip_data["description"]
		session['name'] = name
		session['price'] = price
		session['description'] = description

	else:
		name=''
		price=''
		description=''
		session['name'] = name
		session['price'] = price
		session['description'] = description
		# name = "Not found"
	amazon_data = amazon_scrapping(p_name)
	if(amazon_data):
		a_name = amazon_data["name"]
		a_price = amazon_data["price"]
		a_description = amazon_data["description"]
		session['a_name'] = a_name
		session['a_price'] = a_price
		session['a_description'] = a_description

	else:
		a_name=''
		a_price=''
		a_description=''
		session['a_name'] = a_name
		session['a_price'] = a_price
		session['a_description'] = a_description
		# a_name = "Not found"
	return render_template('products_final.html',flip_name = name,flip_price=price,flip_des=description ,amazon_name = a_name,amazon_price=a_price,amazon_des=a_description )


@app.route("/download_graph",methods=['GET','POST'])
def download_graph():
	global name
	if request.method == "POST":
		print("hey my name is : ",name)
		path = 'graph_images/iphone732.png'
		return send_file(path,as_attachment=True)

@app.route('/predict',methods=['GET','POST'])
def predict():
	with open('icomp/model_predict','rb') as f:
		mp = pickle.load(f)
	if request.method == "POST":
		value = request.form["prediction"]
		l = value.split('-')
		l = [int(num) for num in l]
		l=l[::-1]
		l=[l]
		pred  = int(mp.predict(l)[0])
		print(pred)
		return render_template('products_final.html',pred = pred,date=value, flip_name = session['name'],flip_price=session['price'],flip_des=session['description'] ,amazon_name = session['a_name'],amazon_price=session['a_price'],amazon_des=session['a_description'])
	# features = request.form.values()
	# print(features)

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

@app.route("/admin",methods=['GET','POST'])
def admin():
	if request.method == 'POST':
		if current_user.is_authenticated:
			user = User.query.filter_by(username = 'smit.ds').first()
			if int(user.id) == int(current_user.get_id()):
				news_data = news_scrapping()
				news_data_title1 = news_data['title'][0].strip()
				news_data_title2 = news_data['title'][1].strip()
				news_data_title3 = news_data['title'][2].strip()
				news_data_link1 = news_data['link'][0]
				news_data_link2 = news_data['link'][1]
				news_data_link3 = news_data['link'][2]
				news_data_content1 = news_data['content'][0]
				news_data_content2 = news_data['content'][1]
				news_data_content3 = news_data['content'][2]
				news_object_1 = News(title=news_data_title1,content=news_data_content1)
				news_object_2 = News(title=news_data_title2,content=news_data_content2)
				news_object_3 = News(title=news_data_title3,content=news_data_content3)
				db.session.add(news_object_1)
				db.session.add(news_object_2)
				db.session.add(news_object_3)
				db.session.commit()
				print("All record added ")
				return render_template('admin.html')
			else:
				print("In your face!")

		return render_template('admin.html')
	return render_template('admin.html')
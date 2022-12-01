import os
import secrets
from PIL import Image
from flask import render_template,url_for,flash, redirect,request,send_from_directory,abort
from giveaway.forms import RegistrationForm, LoginForm, UpdateAccountForm,LinkForm
from giveaway.models import User,Post
from giveaway.controller import  Lottory
from giveaway import app,db,bcrypt
from flask_login import login_user,current_user,logout_user,login_required
from pay_ir.api.client import PayIrClient
import random
import xlsxwriter
import time

pay_ir_client = PayIrClient('test')
lottory = Lottory



#Create Home page----------------------------------------------------------------------------------------
@app.route('/')
def main():
   return render_template('hom-page.html',title='homepage')

#Create register page and logics-------------------------------------------------------------------------
@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('your_plan'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hased_password = bcrypt.generate_password_hash(form.password.data).decode('utf_8')
        user = User(username=form.username.data,email=form.email.data, password=hased_password)
        db.session.add(user)
        db.session.commit()
        flash("your account has been created ! you can log in now",'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registerations', form=form)

#Create login page and logics---------------------------------------------------------------------------
@app.route('/login',methods=['GET','POST'])
def login ():
    if current_user.is_authenticated:
        return redirect(url_for('your_plan'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('your_plan'))
        else:
            flash('Login unsuccessful , Please check your email and password', 'danger')    
    return render_template('login.html', title='login', form=form)

#page logout---------------------------------------------------------------------------------------------
@app.route('/logout')
def logout():
    logout_user()
    return redirect (url_for('main'))

#Saving picture function----------------------------------------------------------------------------------
def save_pic(form_picture):
    #To reduce picture size
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(form_picture.filename)
    picture_fn =random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

#Creating Account info page-------------------------------------------------------------------------------
@app.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        #Insert owners picture database
        if form.picture.data:
             picture_file = save_pic(form.picture.data)
             current_user.image_file = picture_file         
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='profile_pics/'+ current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

#Create All plans page------------------------------------------------------------------------------------
@app.route('/plans')
@login_required
def your_plan():
    return render_template('plans.html',title='your-plans')

#Random number genrator-----------------------------------------------------------------------------------------
def random_genarator(min,max):
    random_number = random.randrange(min,max)
    return random_number

#History page data insertion function for All plans----------------------------------------------------
def user_database_insert(form, data_type):
        if form.validate_on_submit():
            url = Post(user_username=current_user.username,
                    type= data_type,
                    tag_mention_followers_urls= form.link.data ,
                    counts=1,
                    author=current_user)
            db.session.add(url)
            db.session.commit()
            
#winner maker -------------------------------------------------------------
def winner_maker (name_of_winner):
        lucky_number = random_genarator(0, len(name_of_winner)+1)
        time.sleep(5)
        winner = name_of_winner[lucky_number]
        print(winner)
        return winner
    
#Create plan followers and page----------------------------------------------------------------------------------
@app.route('/followers-plan',methods=['GET','POST'])
@login_required
def followers_plan():
    form = LinkForm()
    user_database_insert(form,"followers_plan")
    if form.link.data:
        lottory.log_in()
        followers_count=lottory.get_followers(form.link.data)
        print(followers_count)
        time.sleep(5)
        # Mock version of pay.ir
        """
        if 'K' in followers_count or 'M' in followers_count:
            pay_ir_client.init_transaction(10000, 'http://localhost:5000', factor_number=None, mobile=None, description=None)
        elif int(followers_count) > 100:
            pay_ir_client.init_transaction(10000, 'http://localhost:5000', factor_number=None, mobile=None, description=None)
        """
        time.sleep(6)
        name_of_winner= lottory.countinue_on_followers(form.link.data)
        winner = winner_maker(name_of_winner)
        lottory.close_window(5) 
        return render_template('winners.html', title='result', form=winner)
    return render_template('plans_form.html', title='byfollowers', form=form)

#Create plan likers------------------------------------------------------------------------------------------
@app.route('/likers-plan',methods=['GET','POST'])
@login_required
def likers_plan():
    form = LinkForm()
    user_database_insert(form,"likers_plan")
    if form.link.data:
        lottory.log_in()
        likers_count=lottory.get_likers(form.link.data)
        print(likers_count)
        # Mock version of pay.ir
        """
        if "," in likers_count:
            pure_one = likers_count.split(',')
            final_count = pure_one[0]+pure_one[1]
        if int(final_count) > 100:
             pay_ir_client.init_transaction(10000, 'http://localhost:5000', factor_number=None, mobile=None, description=None)
        """
        time.sleep(6)
        name_of_winner = lottory.countinue_on_likers(form.link.data)
        winner = winner_maker(name_of_winner)
        lottory.close_window(5) 
        return render_template('winners.html', title='result', form=winner)
    return render_template('plans_form.html', title='byliks', form=form)

#Create plan comments and page------------------------------------------------------------------------------------
@app.route('/comments-plan',methods=['GET','POST'])
@login_required
def comments_plan(type='comments_plan'):
    form = LinkForm()
    user_database_insert(form,"comments_plan_link")
    if form.link.data:
        lottory.log_in()
        final_list= lottory.get_comments_tags(form.link.data,type)

        # Mock version of pay.ir
        """     
        if len(final_list)> 100:
            pay_ir_client.init_transaction(10000, 'http://localhost:5000', factor_number=None, mobile=None, description=None)
        time.sleep(5)
        """
        winner = winner_maker(final_list)   
        lottory.close_window(5)
        excel_data()
        return render_template('winners.html', title='result', form=winner)
    return render_template('plans_form.html', title='byComments', form=form)


#Create plan tags and page---------------------------------------------------------------------------------
@app.route('/tags-plan',methods=['GET','POST'])
@login_required
def tags_plan(type='tags_plan'):
    return comments_plan(type)

#Create plan combnation and page-----------------------------------------------------------------------------
@app.route('/combnation-plan',methods=['GET','POST'])
@login_required
def combnation_plan():
    form = LinkForm()
    user_database_insert(form,"comments_plan")
    if form.link.data:
        lottory.log_in()
        combine_list = lottory.get_combine(form.link.data)
        # Mock version of pay.ir
        """
        if len(combine_list)> 100:
            pay_ir_client.init_transaction(10000, 'http://localhost:5000/combnation-plan', factor_number=None, mobile=None, description=None)
        """
        time.sleep(6)
        winner = winner_maker(combine_list)
        lottory.close_window(5)
        return render_template('winners.html', title='result', form=winner)   
    return render_template('plans_form.html', title='byTagsandComments', form=form)


#History page-------------------------------------------------------------------------------------------------------------
@app.route("/post/history")
@login_required
def my_post():
    history = Post.query.filter_by(user_username=current_user.username).all()
    return render_template('history.html', title="history", history=history)


#Create an excel file in static directory -----------------------------------------------------------------------------------------------------------
def excel_data():
    workbook = xlsxwriter.Workbook('giveaway/static/cxcel_file/your_data.xlsx')
    worksheet = workbook.add_worksheet("Data")
    cell_format_headers = workbook.add_format()
    cell_format_headers.set_bold()
    cell_format_headers.set_align('center')
    cell_format_headers.set_bg_color('#ADD8E6')
    worksheet.write('A1','username',cell_format_headers)
    worksheet.write('B1','Tags or Comments and Link',cell_format_headers)
    worksheet.write('C1','counts',cell_format_headers)
    post = Post.query.filter_by(author = current_user).all()
    rowIndex = 2
    for element in post:
        worksheet.write('A'+str(rowIndex),element.user_username)
        worksheet.write('B'+str(rowIndex),element.tag_mention_followers_urls)
        worksheet.write('C'+str(rowIndex),element.counts)
        rowIndex +=1
    worksheet.set_column(0,1,width=20)
    worksheet.set_column(1,1,width=100)
    workbook.close()

#Download page-----------------------------------------------------------------------------------------------------------------------------------------
@app.route('/download/data')
@login_required
def get_file():
    try:
        return send_from_directory(app.config["CLIENT_CSV"], path='your_data.xlsx', as_attachment=True)
    except FileNotFoundError :
        abort(404)    
 



    
    

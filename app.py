# from flask import Flask,render_template,request,flash,url_for,redirect
# from otp import genotp
# from cmail import sendmail
# import mysql.connector
# mydb=mysql.connector.connect(host='localhost',
# user='root',
# password='lbnagar@135',
# db='ecommerce'
# )
# app=Flask(__name__)
# app.secret_key='hbhBbkNNF'
# @app.route('/',methods=['GET','POST'])
# def home():
#     return render_template('homepage.html')
# @app.route('/reg',methods=['GET','POST'])
# def register():
#     if request.method=="POST":
#         username=request.form['username']
#         mobile=request.form['mobile']
#         email=request.form['email']
#         address=request.form['address']
#         password=request.form['password']
#         cursor=mydb.cursor()
#         cursor.execute('select email from signup')
#         data=cursor.fetchall()
#         cursor.execute('select mobile from signup')
#         edata=cursor.fetchall()
#         if(mobile,)in data:
#             flash('user already exist')
#             return render_template('register.html')
#         if(email,)in data:
#             flash('Email address already exists')
#             return render_template('register.html')
#         cursor.close()
#         otp=genotp()
#         subject='thanks for registering to the apllication'
#         body=f'use this otp to register {otp}'
#         sendmail(email,subject,body)
#         return render_template('otp.html',otp=otp,username=username,mobile=mobile,email=email,address=address,password=password)
#     else:
#         return render_template('registetr.html') 

# @app.route('/otp/<otp>/<username>/<mobile>/<email>/<address>/<password>',methods=['GET','POst'])
# def otp(otp,username,mobile,email,address,password):
#     if request.method=='POST':
#         uotp=request.form['otp']
#         if otp==uotp:
#             cursor=mydb.cursor()
#             lst=[username,mobile,email,address,password]
#             query='insert into signup values(%s,%s,%s,%s,%s)'
#             cursor.execute(query,lst)
#             mydb.commit()
#             cursor.close()
#             flash('Details registered')
#             return redirect("login")
#         else:
#             flash('wrong otp')
#             return render_template('otp.html',otp=otp,username=username,mobile=mobile,email=email,address=address,password=password)
#     render_template(otp.html)

# @app.route('/login',methods=['GET','POST'])
# def login():
#     if request.method=="POST":
#         username=request.form['username']
#         password=request.form['password']
#         cursor=mydb.cursor()
#         cursor.execute('select count(*) from signup where username=%s and password=%s',[username,password])
#         count=cursor.fetchone()
#         print(count)
#         if count==0:
#             flash('Invalid email or password')
#             return render_template('login.html')
#         else:
#             session['user']=username
#             if not session.get(username):
#                 session[username]={}
#             return redirect(url_for('home'))
#     return render_template('login.html')
# @app.route('/logout')
# def logout():
#     if session.get('user'):
#         session.pop('user')
#         return redirect(url_for('home'))
#     else:
#         flash('already logged out!')
#         return redirect(url_for('login'))
# app.run(debug=True) 



from flask import Flask,render_template,request,flash,url_for,session,redirect
from otp import genotp 
from cmail import sendmail
import mysql.connector
import os
from itemid import itemidotp
mydb=mysql.connector.connect(host='localhost',
user='root',
password='lbnagar@135',
db='ecommerce'
)
app=Flask(__name__)
app.secret_key='jnvnkdfjvndjs'
@app.route('/',methods=['GET','POST'])
def home():
    return render_template('homepage.html')
@app.route('/reg',methods=['GET','POST'])
def register():
    if request.method=="POST":
        username=request.form['username']
        mobile=request.form['mobile']
        email=request.form['email']
        address=request.form['address']
        password=request.form['password']
        cursor=mydb.cursor()
        cursor.execute('select email from signup')
        data=cursor.fetchall()
        cursor.execute('select mobile from signup')
        edata=cursor.fetchall()
        if(mobile,)in edata:
            flash('User already exist')
            return render_template('register.html')
        if(email,)in data:
            flash('Email address already exists')
            return render_template('register.html')
        cursor.close() 
        otp=genotp()
        subject='thanks for registering to the application'
        body=f'use this otp to register {otp}'
        sendmail(email,subject,body)
        return render_template('otp.html',otp=otp,username=username,mobile=mobile,email=email,address=address,password=password)
    else:
        return render_template('register.html')
@app.route('/otp/<otp>/<username>/<mobile>/<email>/<address>/<password>',methods=['GET','POST'])
def otp(otp,username,mobile,email,address,password):
    if request.method=='POST':
        uotp=request.form['otp']
        if otp==uotp:
            cursor=mydb.cursor()
            lst=[username,mobile,email,address,password]
            query='insert into signup values(%s,%s,%s,%s,%s)'
            cursor.execute(query,lst)
            mydb.commit()
            cursor.close()
            flash('Details registered')
            return redirect('login')
        else:
            flash('Wrong otp')
            return render_template('otp.html',otp=otp,username=username,mobile=mobile,email=email,address=address,password=password)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        cursor=mydb.cursor()
        cursor.execute('select count(*) from signup where username=%s and \
        password=%s',[username,password])
        count=cursor.fetchone()
        print(count)
        if count==0:
            flash('Invalid email or password')
            return render_template('login.html')
        else:
            session['user']=username
            if not session.get(username):
                session[username]={}
            return redirect(url_for('home'))
    return render_template('login.html')
@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')
        return redirect(url_for('home1'))
    else:
        flash('already logged out!')
        return redirect(url_for('login'))

@app.route('/additems',methods=['GET','POST'])
def additems():
    if request.method=="POST":
        name=request.form['name']
        discription=request.form['desc']
        quantity=request.form['qty']
        category=request.form['category']
        price=request.form['price']
        image=request.files['image']
        valid_categories=['electronics','grocery','fashion','home']
        if category not in valid_categories:
            flash('Invalid category.Please select a valid option.')
            return render_template('items.html')
        cursor=mydb.cursor()
        idotp=itemidotp()
        filename=idotp+'.jpg'
        cursor.execute('insert into additems(itemid,name,discription,qty,category,price) values(%s,%s,%s,%s,%s,%s)',[idotp,name,discription,quantity,category,price])
        mydb.commit()
        path=os.path.dirname(os.path.abspath(__file__))
        static_path=os.path.join(path,'static')
        image.save(os.path.join(static_path,filename))
        flash('Item added successfuly!s')
    return render_template('items.html')
@app.route('/dashboardpage')
def dashboardpage():
    cursor=mydb.cursor()
    cursor.execute('select *from additems')
    items=cursor.fetchall()
    return render_template('dashboard.html',items=items)
@app.route('/status')
def status():
    cursor=mydb.cursor()
    cursor.execute('select * from additems')
    items=cursor.fetchall()
    return render_template('status.html',items=items)
@app.route('/updateproducts/<itemid>',methods=['GET','POST'])
def updateproducts(itemid):
    cursor=mydb.cursor()
    cursor.execute('select name,discription,qty,category,price from additems where itemid=%s',[itemid])
    items=cursor.fetchone()
    cursor.close()
    if request.method=="POST":
        name=request.form['name']
        discription=request.form['desc']
        quantity=request.form['qty']
        category=request.form['category']
        price=request.form['price']
        cursor=mydb.cursor()
        cursor.execute('update additems set name=%s,discription=%s,qty=%s,category=%s,price=%s where itemid=%s',[name,discription,quantity,category,price,itemid])
        mydb.commit()
        cursor.close()
    return render_template('updateproducts.html',items=items)

@app.route('/deleteproducts/<itemid>')
def deleteproducts(itemid):
    cursor=mydb.cursor()
    cursor.execute('delete from additems where itemid=%s',[itemid])
    mydb.commit()
    cursor.close()
    path=os.path.dirname(os.path.abspath(__file__))
    static_path=os.path.join(path,'static')
    filename=itemid+'.jpg'
    os.remove(os.path.join(static_path,filename))
    flash('deleted')
    return redirect(url_for('status'))
@app.route('/cart/<itemid>/<name>/<int:price>',methods=['GET','POST'])
def cart(itemid,name,price):
    #purpose:To add items to a user's cart stored in the sesion
    if session.get('user'):
        if request.method=='POST':
            qty=int(request.form['qty'])
            if itemid not in session[session.get('user')]:#if the items is not in cart
                session[session.get('user')][itemid]=[name,qty,price]
                session.modified=True
                flash(f'{name} added to cart')
                return recirect(url_for('viewcart'))
            session[session.get('user')][itemid][1]+=qty#if item exists,increments the qty
            session.modified=True
            flash('Item already in cart quantity increased to +{qty}')
    return redirect(url_for('login'))
def viewcart():# to display the items in the cart
    if not session.get('user'):#checks if the user is logged in 
        return redirect(url_for('login'))
    # items=session.get(session.get('user'))if session.get(session.get('user')) else 'empty'
    # if items=='empty':
    #     return 'no products in cart'
    # return render_template('cart.html',items=items)
    user_cart=session.get(session.get('user'))
    if not user_cart:
        items="empty"
    else:
        items=user_cart
    if items=="empty":
        return '<h3> your cart is empty</h3>'
    return render_template('cart.html',items=items)



@app.route('/addcart/<itemid>/<name>/<category>/<price>/<quantity>',methods=['GET','POST'])
def addcart(itemid,name,category,price,quantity):
    if not session.get('user'):
        return redirect(url_for('login'))
    else:
        print(session)
        if itemid not in session.get(session['user'],{}):
            if session.get(session['user']) is None:
                session[session['user']]={}
            session[session['user']][itemid]=[name.price,1,f'{itemid}.jpg',category]
            session.modified=True
            flash(f'{name} added to cart')
            return redirect(url_for('index'))
        session[sessiom['user']][itemid][2]==1

def dis(itemid):
    cursor=mydb.cursor()
    cursor.execute('select * from additems where itemid=%s,[itemid]')
    items=cursor.fetchone()
    return render_template('display.html',items=items)


#for payment -->id,name,price
@app.route('/pay/<item>/<name>/<price>',methods=['GET','POST'])
def pay(itemid,name,price):
    try:
        # Get the quantity from the form
        qyt=int(request.form['qyt'])
        amount=price*100
        # calculate the total amount in paise (price is in rupees)
        total_price=amount*qyt
        print(amount,qty,total_price)
        print(f'creating payment for item:{itemid},name:{name},price:{total_price}')
        #create Razarpay order
        order=client.order.create({
            'amount':total_price,
            'currency':'INR',
            'payment_capture':'1'

        })
        print(f'Order created:{order}')
        return render_template('pay.html',order=order,itemid=itemid,name=name,price=total_price,qyt=qyt)
    except Exeception as e:
        #log the error and return a 400 response
        print(f'Error creating order:{str(e)}')
        return str(e),400
@app.route('/success',methods=['POST'])
def success():
    payment_id=request.form.get('razorpay_payment_id')
    order_id=request.form.get('razorpay_order_id')
    signature=request.form.get('razorpay_signature')
    name=request.form.get('name')
    itemid=request.form.get('itemid')
    total_price=request.form.get('total_price')
    qty=request.form.get('qty')


    params_dict={
        'razorpay_order_id':order_id,
        'razorpay_payment_id':payment_id,
        'razorpay_signature':signature
    }
    try:
        client.utility.verify_payment_signature(params_dict)
        cursor=mydb.cursur(buffered=True)
        cursor.execute('insert into orders(itemid,item_name,total_price,user,qty)values(%s,%s,%s,%s,%s)',
        [itemid,name,total_price,session.get('user'),qyt])
        mydb.commit()
        cursor.close()
        flash('Order placed sucessfully')
        return 'orders'
    except razorpay.errors.SignatureVerficationError:
        return 'payment verification failed',400
@app.route('/orders')
def orders():
    if session.get('user'):
        user=session.get('user')
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select *from orders where user=%s',[user])
        data=cursor.fetchall()
        cursor.close()
        return render_template('orderdisplay.html',data=data)
    else:
        return redirect(url_for('login'))
if __name__=='_main_':        
app.run(debug=True)
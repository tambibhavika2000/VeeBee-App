from flask import Flask,render_template,request,redirect,session
import mysql.connector
import os

app=Flask(__name__)
app.secret_key=os.urandom(24)

conn= mysql.connector.connect(host="localhost",user="root",password="bhavikatambi",database="details")
cursor=conn.cursor()

@app.route('/')
def home():
    if 'id' in session:
        return redirect('/home')
    else:
        return render_template('first.html')

@app.route('/register')
def register():
    return render_template('registers.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/home')
def option():
    return render_template('home.html')

@app.route('/login_validation', methods=['POST'])
def valid():
    email=request.form.get('email')
    psw=request.form.get('psw')

    cursor.execute("""SELECT * FROM `users` where `email` like '{}' and `password` like '{}'""".format(email,psw))
    users=cursor.fetchall()
    session['name']= users[0][1]
    session['email']= users[0][2]
    if len(users)>0:
        session['id']=users[0][0]
        return redirect('/home')
    else:
        return redirect('/register')


@app.route('/profile')
def profile():
    return render_template('profile.html', name=session['name'], email=session['email'])

@app.route('/logout')
def logout():
    try:
        session.pop('id')
    except:
        return redirect('/index')
    return redirect('/index')

@app.route('/add_user', methods=['POST'])
def add_user():
    name=request.form.get('uname')
    email=request.form.get('ename')
    upsw=request.form.get('upsw')
    cpsw=request.form.get('cpsw')
    if upsw==cpsw:
        try:
            cursor.execute("""INSERT INTO `users` (`id`,`name`,`email`,`password`) values
            (NULL,'{}','{}','{}')""".format(name,email,upsw))
            conn.commit()
            return redirect('/index')
        except:
            return ("User already exist . Login with your credentials")
    else:
        return "password does not match"


if __name__=="__main__":
    app.run(debug=True)
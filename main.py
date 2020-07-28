from flask import Flask,render_template,request,redirect,session
import mysql.connector
import os

app=Flask(__name__)
app.secret_key=os.urandom(24)

conn= mysql.connector.connect(host="localhost",user="root",password="bhavikatambi",database="details")
cursor=conn.cursor()

@app.route('/')
def index():
    if 'id' in session:
        return redirect('/option')
    else:
        return render_template('index.html')

@app.route('/register')
def register():
    return render_template('registers.html')

@app.route('/option')
def option():
    return render_template('option.html')

@app.route('/login_validation', methods=['POST'])
def valid():
    email=request.form.get('email')
    psw=request.form.get('psw')

    cursor.execute("""SELECT * FROM `users` where `email` like '{}' and `password` like '{}'""".format(email,psw))
    users=cursor.fetchall()
    if len(users)>0:
        session['id']=users[0][0]
        return redirect('/option')
    else:
        return redirect('/register')

@app.route('/add_user', methods=['POST'])
def add_user():
    name=request.form.get('uname')
    email=request.form.get('ename')
    upsw=request.form.get('upsw')
    cpsw=request.form.get('cpsw')
    if upsw==cpsw:
        cursor.execute("""INSERT INTO `users` (`id`,`name`,`email`,`password`) values
        (NULL,'{}','{}','{}')""".format(name,email,upsw))
        conn.commit()
        return redirect('/')
    else:
        return redirect('/register')


if __name__=="__main__":
    app.run(debug=True)
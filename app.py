from flask import Flask, render_template, request, session
import mysql.connector as mysql 

db=mysql.connect(
    host='localhost',
    user='root',
    password='Naveenkumar@60',
    database='db'
)

cur=db.cursor()

app=Flask(__name__) 
app.secret_key="Naveen"

@app.route('/')
def registerPage():
    return render_template('register.html')

@app.route('/login')
def loginPage():
    return render_template('login.html')

@app.route('/registerdata', methods=['POST'])
def registerData():
    r=(request.form['rollno']).upper()
    n=request.form['name']
    p=request.form['password']
    if r and n and p:
        session['rollno'] = r
        sql = 'select rollno from student_info where rollno = %s'
        rno = [(session['rollno'])]
        cur.execute(sql,rno)
        account = cur.fetchone()
        if account:
            if session['rollno'] == account[0]:
                return render_template('register.html',res = "Record Already Exists")
        else:
            storeData(r,n,p)
            res = "Data Collected"
            return render_template('register.html',res = res)
    else:
        abc = "All Fields are MAndatory"
        return render_template('register.html',abc = abc)

@app.route('/logindata', methods=['GET','POST'])
def loginData():
    r=(request.form['rollno']).upper()
    p=request.form['password']
    if r and p:
        session['rollno']=r
        session['password']=p
        sql="SELECT rollno,password FROM student_info where rollno=%s"
        rno=[(session['rollno'])]
        cur.execute(sql,rno)
        account = cur.fetchone()
        print(account)
        if account:
            if  session['rollno'] == account[0] and session['password'] == account[1]:
                return render_template('success.html')
            else:
                result='Invalid Login'
                return render_template('login.html',result=result)
        else:
            result="No Records Found\nPlease Register"
            return render_template('login.html',result=result)
    else:
        return render_template('login.html',result="All Fields are mandatory")
@app.route('/logout')
def logout():
    session.pop('rollno')
    session.pop('password')
    return render_template('login.html')

def storeData(rollno,name,password):
    sql="INSERT INTO student_info(rollno,name,password) VALUES(%s,%s,%s)"
    val=(rollno,name,password)
    cur.execute(sql,val)
    db.commit() 

if __name__=="__main__":
    app.run(debug=True)
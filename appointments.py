from flask import Flask, render_template, json, request, jsonify
from flask_mysqldb import MySQL
from werkzeug import secure_filename
import os

app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'medic'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"
mysql = MySQL(app)

@app.route('/db')
def users():
    cur = mysql.connection.cursor()
	#print "insert_new_user called---insertion happens here"
    cur.execute('''SELECT user, host FROM mysql.user''')
    rv = cur.fetchall()
    return str(rv)
	
@app.route('/')
def index():    
    return "Hello World"
	
@app.route('/adddoctor', methods=['POST'])
def insert_new_user():
    
	
    # read the posted values from the UI
    patient_id = str(request.json['patient_id'])
    patient_name = str(request.json['patient_name'])
    appointment_date = str(request.json['appointment_date'])

    # return user_id
	

    data =(patient_id,patient_name,appointment_date)

    print  request.json['patient_id']
    print  request.json['patient_name']
    print  request.json['appointment_date']
    
    #return json.dumps({'status': "success"})
    medic = mysql.connection
    cur = medic.cursor()
    sql = "INSERT INTO appointment(patient_id,patient_name,appointment_date) VALUES(%s,%s,%s)"
    try:
        cur.execute(sql,data)
        print cur.fetchall
        medic.commit()
    except:
        print "There is an exception !"
        return json.dumps({'status': "failed"})
    result = cur.fetchall
    print result
    # validate the received values
    if patient_id and patient_name and appointment_date:
        return json.dumps({'status': "Appointment fixed"})
    else:
        return json.dumps({'status': "Try some other slot"})
	

if __name__ == '__main__':
    app.run(host="127.0.0.1",port=5000,debug=True)
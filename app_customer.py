from flask import Flask, render_template, request, url_for 
from flask_sqlalchemy import SQLAlchemy
import waitlist_recorder
from waitlist_recorder import Customer
import sqlite3
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URL'] = 'customer.db'
# db = SQLAlchemy(app)

# class Customer(db.Model): 
#     name = db.Column(db.String)
#     conatct = db._Column(db.String)

connection = sqlite3.connect("waitlist.db") 
connection.commit()
cursor = connection.cursor()

@app.route("/")
def home(): 
    return render_template('index.html') 

@app.route('/getnumber', methods = ['GET', 'POST'])
def get_number(): 
    return render_template(
    'getnumber.html'
    ) 

@app.route('/return_user')
def return_user(): 
    return render_template('returnuser.html')

@app.route('/waiting_info/return_user', methods = ['POST'])
def get_return_user(): 
    if request.method == 'POST': 
        cust_contact = request.form['contact']
        num_groups_waiting, waiting_time,  table_size = waitlist_recorder.get_return_user_waiting_num_and_time(cust_contact)
        return render_template("waitinginfo.html",num_groups = num_groups_waiting, time = waiting_time, size = table_size ) 

@app.route('/waiting_info/new_user', methods = ['POST', 'GET'])
def get_waiting_info(): 
    if request.method == "POST":
        name = request.form['name']
        group_size = int(request.form['group_size'])
        contact = request.form['contact']
        cust= Customer(name, contact, group_size)
        waitlist_recorder.insert_customer_info(cust)
        # cursor.execute("INSERT INTO customer_info VALUES (?, ?, ?);", (cust.name, cust.contact, cust.group))
        # connection.commit()
        num_groups_waiting, waiting_time = waitlist_recorder.count_numbers_waiting_and_time(cust)
        table_size = waitlist_recorder.define_table_size(cust)[1]
        return render_template("waitinginfo.html",num_groups = num_groups_waiting, time = waiting_time, size = table_size)


@app.route('/call_table')
def call_large(): 
    waitlist_recorder.call_large_table()

def call_mid(): 
    waitlist_recorder.call_mid_table()

def call_small(): 
    waitlist_recorder.call_small_table() 

if __name__ == '__main__':
    app.run(debug=True, port = 12345)


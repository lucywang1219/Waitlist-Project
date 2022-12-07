from flask import Flask, render_template, request 
import waitlist_recorder
from waitlist_recorder import Customer
import sqlite3
app = Flask(__name__)


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
        waitlist_recorder.get_return_user_waiting_num_and_time(cust_contact)
        if waitlist_recorder.get_return_user_waiting_num_and_time(cust_contact) == None: 
            return render_template('contact_not_found.html')
        else: 
            num_groups_waiting, waiting_time,  table_size = waitlist_recorder.get_return_user_waiting_num_and_time(cust_contact)
            return render_template("waitinginfo.html",num_groups = num_groups_waiting, time = waiting_time, size = table_size ) 

@app.route('/waiting_info/new_user', methods = ['POST', 'GET'])
def get_waiting_info(): 
    if request.method == "POST":
        name = request.form['name']
        group_size = int(request.form['group_size'])
        contact = request.form['contact']
        waitlist_recorder.validate_contact(contact)
        if waitlist_recorder.validate_contact(contact) == None: 
            return render_template('invalid_contact.html')
        else: 
            cust= Customer(name, contact, group_size)
            waitlist_recorder.insert_customer_info(cust)
            num_groups_waiting, waiting_time = waitlist_recorder.count_numbers_waiting_and_time(cust)
            table_size = waitlist_recorder.define_table_size(cust)[1]
            return render_template("waitinginfo.html",num_groups = num_groups_waiting, time = waiting_time, size = table_size)


if __name__ == '__main__':
    app.run(debug=True, port = 12345)


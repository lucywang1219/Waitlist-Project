from flask import Flask, render_template, request
import waitlist_recorder
from waitlist_recorder import Customer
import sqlite3
app = Flask(__name__)

@app.route("/")
def home(): 
    return render_template('index.html') 

@app.route('/getnumber', methods = ['GET', 'POST'])
def get_number(): 
    return render_template(
    'getnumber.html'
    ) 

def get_waiting_info(): 
    if request.method == "POST":
        name = request.form['name']
        contact = request.form['contact']
        group_size = request.form['group_size']
        cust = Customer(name, contact, group_size) 
        with sqlite3.connect("wailist.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO customer_info VALUES (?, ?, ?);", (cust.name, cust.contact, cust.group))
            
            con.commit()

        # waitlist_recorder.insert_customer_info(cust)
        num_groups_waiting, waiting_time = waitlist_recorder.count_numbers_waiting_and_time(cust)
        table, table_size = waitlist_recorder.define_table_size(cust)
        return render_template("waiting_info.html",num_groups = num_groups_waiting, time = waiting_time, size = table_size)


@app.route('/return_user')
def return_user(): 
    return render_template('returnuser.html')

@app.route('/waiting_info', methods = ['GET', 'POST'])
def get_return_user(): 
    if request.method == 'POST': 
        contact = request.form['contact'] #TODO: no form, what is the name in html? 
        num_groups_waiting, waiting_time,  table_size = waitlist_recorder.get_return_user_waiting_num_and_time(contact)
        return render_template("waiting_info.html",num_groups = num_groups_waiting, time = waiting_time, size = table_size ) 

@app.route('/call_table')
def call_large(): 
    waitlist_recorder.call_large_table()

def call_mid(): 
    waitlist_recorder.call_mid_table()

def call_small(): 
    waitlist_recorder.call_small_table() 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=50000)
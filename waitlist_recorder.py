
"""
1. customer input: insert customer info into SQL table  
2. return the number of people waiting
3. estimate waiting time 
4. Waiter's end: call next table 
5. After call, the estimated waiting line - 1
6. "Your table is ready" when the people waiting = 0 
7. eliminate that customer from the SQL table 
8. empty the table after 12am everyday 
9. return user: enter contact, chek estimated time and number of groups waiting count_numbers_waiting() 
"""

import sqlite3
from configparser import ConfigParser
import os
from twilio.rest import Client


os.environ['TWILIO_ACCOUNT_SID'] = 'AC4be78e3eaf5d179379fe2a6d63a13600'
os.environ['TWILIO_AUTH_TOKEN'] = '3644e7ada0c92bb6f2eda3b03516d6ec'

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

connection = sqlite3.connect("waitlist.db")
cursor = connection.cursor()
# cursor.execute("CREATE TABLE customer_info (name TEXT, contact TEXT, group_size INTEGER)")
connection.commit()

small_table = [1,2,3]
mid_table = [4,5,6]
large_table = [7,8,9,10]

class Customer: 
    def __init__(self, customer_name, customer_contact, group_size): 
        self.name = customer_name 
        self.contact  = customer_contact
        self.group = group_size 

"""Get customer inputs """

def insert_customer_info(cust): 
    """insert customer information """
    cursor.execute("INSERT INTO customer_info VALUES (?, ?, ?);", (cust.name, cust.contact, cust.group))

def define_table_size(cust): 
    if 1 <= cust.group <= 3: 
        table = small_table
        table_size = 'small'
    elif 4<= cust.group <= 6: 
        table = mid_table
        table_size = 'medium'
    elif cust.group >= 7: 
        table = large_table
        table_size = 'large'
    return table, table_size  

def count_numbers_waiting_and_time(cust): 
    """assume table turnover rate is 10 minutes"""
    # if 1 <= cust.group <= 3: 
    #     table = small_table
    # elif 4<= cust.group <= 6: 
    #     table = mid_table
    # elif cust.group >= 7: 
    #     table = large_table
    table, table_size = define_table_size(cust)
    cursor.execute("SELECT * FROM customer_info WHERE group_size IN {}".format(str(tuple(table))))
    num_groups_waiting = len(cursor.fetchall())
    waiting_time = num_groups_waiting * 10 
    return num_groups_waiting, waiting_time
  

def call_large_table(): 
    cursor.execute("SELECT * FROM customer_info WHERE group_size >= 7 ")
    customer = list(cursor.fetchone())
    cust = Customer(customer[0], customer[1], customer[2])

    message = client.messages \
        .create(
            body=f'Dear {cust.name}, your table is ready.',
            from_='+13087734285',
            to='+13399330492'
        )

    print(message.sid)

def call_mid_table(): 
    cursor.execute("SELECT * FROM customer_info WHERE group_size >= 4 AND group_size <= 6 ")
    called_cust = list(cursor.fetchone())
    customer = list(cursor.fetchone())
    cust = Customer(customer[0], customer[1], customer[2])

    message = client.messages \
        .create(
            body=f'Dear {cust.name}, your table is ready.',
            from_='+13087734285',
            to='+13399330492'
        )

    print(message.sid)

def call_small_table(): 
    cursor.execute("SELECT * FROM customer_info WHERE 1 <= group_size <= 3 ")
    called_cust = list(cursor.fetchone())
    customer = list(cursor.fetchone())
    cust = Customer(customer[0], customer[1], customer[2])

    message = client.messages \
        .create(
            body=f'Dear {cust.name}, your table is ready.',
            from_='+13087734285',
            to= '+1'+ {cust.contact}
        )

    print(message.sid)

def delete_customer(called_cust): 
    cursor.execute("DELETE FROM customer_info WHERE contact = ?", [called_cust[1]]) 

def get_return_user_waiting_num_and_time(contact): 
    cursor.execute("SELECT * FROM customer_info WHERE contact = ?", [contact]) 
    cust_list = (cursor.fetchone())
    cust = Customer(cust_list[0], cust_list[1], cust_list[2])
    table_size = define_table_size(cust) 
    num_groups_waiting, waiting_time = count_numbers_waiting_and_time(cust)
    return num_groups_waiting, waiting_time, table_size


def main(): 
    # customer_name = input("customer name: ")
    # customer_contact = input("Your contact: ")
    # customer_size = int(input("Your group size: ")) 
    # cust = Customer(customer_name, customer_contact, customer_size)
    # insert_customer_info(cust)
    # print(count_numbers_waiting_and_time(cust))
    # print(get_return_user_waiting_num_and_time(cust))
    # cursor.execute("DELETE FROM customer_info WHERE name = '4'")
    
   
    print(call_large_table())
    # print(call_mid_table())
    # print(call_small_table())

    # contact = input("Your contact: ")
    # print(get_return_user_waiting_num_and_time(contact))
    connection.commit()

if __name__ == "__main__":
    main()
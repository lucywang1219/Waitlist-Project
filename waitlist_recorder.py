
"""
1. customer input: insert customer info into SQL table  
2. return the number of people waiting
3. estimate waiting time 
4. Waiter's end: call next table 
5. After call, the called customer is eliminated from db 
6. "Your table is ready" when the waiter call the nest table 
7. return user: enter contact, check estimated time and number of groups waiting count_numbers_waiting() 
8. ask users to enter a valid number if entered number is not valid (for new users) or not found in db (for return users). 
"""

import sqlite3
import os
from twilio.rest import Client

"""
These should be your own Twilio account ID and token, where are stored as environment variables. """
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

"""connect database"""
connection = sqlite3.connect("waitlist.db",check_same_thread=False)
cursor = connection.cursor()

"""use the code below to create a table"""
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


def insert_customer_info(cust):
    """insert customer information """
    cursor.execute("INSERT INTO customer_info VALUES (?, ?, ?);", (cust.name, cust.contact, cust.group))
    connection.commit()

def define_table_size(cust): 
    if 1 <= cust.group <= 3: 
        table = small_table
        table_size = 'Small'
    elif 4<= cust.group <= 6: 
        table = mid_table
        table_size = 'Medium'
    elif cust.group >= 7: 
        table = large_table
        table_size = 'Large'
    return table, table_size  

def count_numbers_waiting_and_time(cust): 
    """assume table turnover rate is 10 minutes"""
    table = define_table_size(cust)[0]
    cursor.execute("SELECT * FROM customer_info WHERE group_size IN {}".format(str(tuple(table))))
    num_groups_waiting = len(cursor.fetchall())
    waiting_time = num_groups_waiting * 10 
    return num_groups_waiting, waiting_time
  

def send_message_twilio(cust):
    """send message to the customer. Replace the 'from_=' number with your own digital number. """
    contact = '+1' + cust.contact
    print(contact)
    message = client.messages \
        .create(
            body=f'Dear {cust.name}, your table is ready.',
            from_='+13087734285',
            to= {contact}
        )
    print(message.sid)
    print(f'Dear {cust.name}, your table is ready.')

def call_large_table(): 
    """call the next table and send the customer an SMS message """
    cursor.execute("SELECT * FROM customer_info WHERE group_size >= 7 ")
    customer = cursor.fetchone()
    if customer == None: 
        return None 
    else: 
        customer = list(customer)
        cust = Customer(customer[0], customer[1], customer[2])
        print(customer)
        send_message_twilio(cust)
        delete_customer(customer)

def call_mid_table(): 
    cursor.execute("SELECT * FROM customer_info WHERE group_size >= 4 AND group_size <= 6 ")
    customer = cursor.fetchone()
    if customer == None: 
        return None 
    else: 
        customer = list(customer)
        cust = Customer(customer[0], customer[1], customer[2])
        print(customer)
        send_message_twilio(cust)
        delete_customer(customer)

def call_small_table(): 
    cursor.execute("SELECT * FROM customer_info WHERE 1 <= group_size <= 3 ")
    customer = cursor.fetchone()
    if customer == None: 
        return None 
    else: 
        customer = list(customer)
        cust = Customer(customer[0], customer[1], customer[2])
        print(customer)
        send_message_twilio(cust)
        delete_customer(customer)

def delete_customer(called_cust):
    """
    Parameters:
        called_cust: a tuple
    """ 
    print(f'deleting {called_cust}')
    cursor.execute("DELETE FROM customer_info WHERE contact = ?", [called_cust[1]]) 
    connection.commit() 
    

def get_return_user_waiting_num_and_time(contact): 
    cursor.execute("SELECT * FROM customer_info WHERE contact = ?", [contact]) 
    cust_list = (cursor.fetchone())
    if cust_list == None: 
        return None
    else: 
        cust = Customer(cust_list[0], cust_list[1], cust_list[2])
        table_size = define_table_size(cust)[1]
        num_groups_waiting, waiting_time = count_numbers_waiting_and_time(cust)
        return num_groups_waiting, waiting_time, table_size

def get_all():
    """Return all customers' info"""
    print('Getting all customer from database')
    cursor.execute("SELECT * FROM customer_info")
    all_customers = cursor.fetchall() # list of tuples [(name, contact, size), ()]
    return all_customers

def validate_contact(contact):  
    """make sure the phone number entered is valid"""
    try: 
        phone_number = client.lookups \
                    .v1 \
                     .phone_numbers(f'{contact}') \
                    .fetch(country_code='US')

        print(phone_number.phone_number)
    except Exception: 
        return None 

def main(): 
    """testing code """
    # customer_name = input("customer name: ")
    # customer_contact = input("Your contact: ")
    # customer_size = int(input("Your group size: ")) 
    # cust = Customer(customer_name, customer_contact, customer_size)
    # insert_customer_info(cust)

    # print(count_numbers_waiting_and_time(cust))
    # print(get_return_user_waiting_num_and_time(cust))
    # cursor.execute("DELETE FROM customer_info WHERE name = '4'")
    
    # print(call_large_table())
    # print(call_mid_table())
    # print(call_small_table())

    # contact = input("Your contact: ")
    # print(get_return_user_waiting_num_and_time(contact))


if __name__ == "__main__":
    main()
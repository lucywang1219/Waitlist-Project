from flask import Flask, render_template, request
import waitlist_recorder
from waitlist_recorder import Customer
app = Flask(__name__, template_folder = 'templates', static_folder= 'static')

@app.route('/')
def call_table(): 
    return render_template('calltable.html')

def call_large(): 
    waitlist_recorder.call_large_table()

def call_mid(): 
    waitlist_recorder.call_mid_table()

def call_small(): 
    waitlist_recorder.call_small_table() 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=54321)
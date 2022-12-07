from flask import Flask, render_template, request
import waitlist_recorder
from waitlist_recorder import Customer
app = Flask(__name__, template_folder = 'templates', static_folder= 'static')

CALL_FUNCTIONS = {
    'large': waitlist_recorder.call_large_table,
    'mid': waitlist_recorder.call_mid_table,
    'small': waitlist_recorder.call_small_table,
}

@app.route('/',  methods = ['POST', 'GET'])
def call_table(): 
    if request.method == 'POST':
        size = request.form['size']
        CALL_FUNCTIONS[size]()
        all_customers = waitlist_recorder.get_all()
        if CALL_FUNCTIONS[size]() == None: 
            return render_template('no_next_table.html', size = size, customers=all_customers)
        else: 
            print(all_customers)
            return render_template('all_customers.html', customers=all_customers)

    return render_template('calltable.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=54321)
#!/usr/bin/python3
'''A python script that starts a Flask web application'''
from flask import Flask

# create a Flask application instance
app = Flask(__name__)


# route for root URL
@app.route('/', strict_slashes=False)
def hello_HBNB():
    '''Displays 'Hello HBNB!'
    '''
    return 'Hello HBNB!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

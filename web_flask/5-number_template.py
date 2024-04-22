#!/usr/bin/python3
'''A python script that starts a Flask web application'''
from flask import Flask, render_template

# create Flask application instance
app = Flask(__name__)


# route for the root URL
@app.route('/', strict_slashes=False)
def hello_HBNB():
    '''Displays 'Hello HBNB!'
    '''
    return 'Hello HBNB!'


# route for /hbnb
@app.route('/hbnb', strict_slashes=False)
def HBNB():
    '''Displays 'HBNB'
    '''
    return 'HBNB'


# route for /c/<text>
@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    '''Displays a text!'''
    text = text.replace('_', ' ')
    return f'C {text}'


# route for /python/<text>
@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_route(text='is cool'):
    '''Displays a text!'''
    text = text.replace('_', ' ')
    return f'Python {text}'


# route for /number/<n>
@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    '''displays a number if number is an int'''
    return f'{n} is a number'


# route for /number_template/<n>
@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template_route(n):
    '''displays a number based on a template'''
    return render_template('5-number.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

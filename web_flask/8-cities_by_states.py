#!/usr/bin/python3
'''A python script that starts a Web Flask application'''
from flask import Flask, render_template
from models import storage
from models.state import State

# create flask app instance
app = Flask(__name__)

# remove current SQLAlchemy session
@app.teardown_appcontext
def remove_session(exception):
    '''Removes the current SQLAlchemy Session'''
    storage.close()

# route for /states_list
@app.route('/cities_by_states', strict_slashes=False)
def cities_states():
    '''Displays a HTML page with states objects'''
    states = storage.all(State).values()
    return render_template('8-cities_by_states.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

#!/usr/bin/python3
'''A python script that starts a Web Flask application'''
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity

# create flask app instance
app = Flask(__name__)


# remove current SQLAlchemy session
@app.teardown_appcontext
def remove_session(exception):
    '''Removes the current SQLAlchemy Session'''
    storage.close()


# route for /states_list
@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    '''Displays a HTML page hbnb_filters'''
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    return render_template(
        '10-hbnb_filters.html', states=states, amenities=amenities
        )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

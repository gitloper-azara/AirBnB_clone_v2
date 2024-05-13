#!/usr/bin/python3
'''A python script that starts a Web Flask application'''
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place

# create flask app instance
app = Flask(__name__)


# remove current SQLAlchemy session
@app.teardown_appcontext
def remove_session(exception):
    '''Removes the current SQLAlchemy Session'''
    storage.close()


# route for /hbnb
@app.route('/hbnb', strict_slashes=False)
def hbnb():
    '''Displays a HTML page hbnb_filters'''
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()
    return render_template(
        '100-hbnb.html', states=states, amenities=amenities, places=places
        )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

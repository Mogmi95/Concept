# -*- coding: utf-8 -*-
"""Game views."""
from flask import Blueprint, render_template

from .models import Idea, Concept

blueprint = Blueprint("game", __name__, url_prefix="/game", static_folder="../static")


@blueprint.route("/")
def guess():
    """Display game."""

    data = create_game_data()
    concept_set = get_set()
    return render_template("game/guess.html", data=data, concept_set=concept_set)

@blueprint.route("/creation")
def creation():
    """Create a new Idea."""

    concept_set = get_set()
    return render_template("game/create.html", concept_set=concept_set)

def create_game_data():
    return '{"idea":{"set":"default","answer":"requin","language":"en-US","concepts":[{"main":6,"is_core":true,"precisions":[20]},{"main":48,"precisions":[23]}]}}'

def get_set():
    current_set = {
        0: {'image': 'object.svg', 'description': ['Object', 'Thing', 'Package']},
        1: {'image': 'person.svg', 'description': ['Person', 'Family', 'Group']},
        2: {'image': 'female.svg', 'description': ['Female', 'Woman' 'Wife', 'Feminine']},
        3: {'image': 'male.svg', 'description': ['Male', 'Man', 'Husband', 'Masculine']},
        4: {'image': 'work.svg', 'description': ['Work', 'Profession', 'Craft']},
        5: {'image': 'recreation.svg', 'description': ['Recreation', 'Sport', 'Activity']},
        #6: {'image': 'wildlife.svg', 'description': ['Wildlife', 'Animal']},
        #7: {'image': 'flora.svg', 'description': ['Flora', 'Nature', 'Plant']},
        #8: {'image': 'literature.svg', 'description': ['Literature', 'Writing', 'Book']},
        #9: {'image': 'music.svg', 'description': ['Music', 'Song', 'Note']},
        #10: {'image': 'theater.svg', 'description': ['Theater', 'Film', 'Camera']},
        #11: {'image': 'arts.svg', 'description': ['Arts', 'Scupture', 'Painting', 'Drawing', 'Comics']},
        #12: {'image': 'television.svg', 'description': ['Television', 'Broadcast', 'Series']},
        #13: {'image': 'title.svg', 'description': ['Title', 'Brand', 'Name']},
        #14: {'image': 'idea.svg', 'description': ['Idea', 'Thought', 'Concept']},
        #15: {'image': 'expression.svg', 'description': ['Expression', 'Quote', 'Speak', 'Word']},
        #16: {'image': 'location.svg', 'description': ['Location', 'Country', 'Flag']},
        #17: {'image': 'building.svg', 'description': ['Building', 'Construction', 'City']},
        #18: {'image': 'date.svg', 'description': ['Date', 'Event', 'Daytime']},
        #19: {'image': 'holidays.svg', 'description': ['Holidays', 'Birthday', 'Celebration']},
        #20: {'image': 'watercraft.svg', 'description': ['Watercraft', 'Maritime', 'Swim']},
        #21: {'image': 'fly.svg', 'description': ['Airborne vehicle', 'Airline', 'Fly']},
        #22: {'image': 'car.svg', 'description': ['Land vehicle', 'Car', 'Ride']},
        #23: {'image': 'tools.svg', 'description': ['Tools', 'Construction']},
        #24: {'image': 'games.svg', 'description': ['Games', 'Toys', 'Youth']},
        #25: {'image': 'clothing.svg', 'description': ['Clothing', 'Accessories', 'Costume']},
        #26: {'image': 'food.svg', 'description': ['Food', 'Nutrition', 'Edible']},
        #27: {'image': 'home.svg', 'description': ['Home', 'Interior', 'Domestic']},



        48: {'image': 'head.svg', 'description': ['Head', 'Face']},
    }
    return current_set
# -*- coding: utf-8 -*-
"""Game views."""
from flask import Blueprint, render_template, request

import base64
import json

from .models import Idea, Concept

blueprint = Blueprint("game", __name__, url_prefix="/game", static_folder="../static")


@blueprint.route("/guess/<conceptcode>")
def guess(conceptcode):
    """Display game."""

    #data = create_game_data()
    data = conceptcode_to_json(conceptcode)
    game_set = get_set()
    return render_template("game/guess.html", data=data, game_set=game_set)

@blueprint.route("/new")
def new():
    """Create a new Idea."""

    concept_set = get_set()
    return render_template("game/create.html", concept_set=concept_set)

@blueprint.route("/api/new", methods=['POST'])
def api_create():
    """API to create a new game."""
    conceptcode = json_to_conceptcode(request.get_json())
    return {"conceptcode": conceptcode}

def json_to_conceptcode(json):
    # Set
    gameset = "0"

    # Language
    language = "en"

    jsonideas = json['game']['ideas']
    ideas = ""
    for idea in jsonideas:
        ideacode = ""
        concepts = idea['concepts']
        concepts.sort(key=lambda concept: concept['pos'])
        for concept in concepts:
            ideacode += "c" + str(concept['id']) + "p" + str(concept['points'])
        ideas += "i" + ideacode

    answer = base64.b64encode(json['game']['answer'].encode("utf-8")).decode("utf-8")
    return f"g{gameset}-{language}-{ideas}-{answer}"

def conceptcode_to_json(conceptcode):
    """
    Parse a conceptcode to create a JSON format game data.

    Format is: g0-en-ic4p1c5p3ic4p1c5p3-FGJIZERGOIERJGIOJSDFIG
        * g = start
        * 0 = set
        * en = locale
        * ic4p1c5p3ic4p1c5p3 = ideas/concepts
            * ic4p1c5p2 = idea with main concept as 4 with 1 point and a secondary concept as 5 with 2 points
        * FGJIZERGOIERJGIOJSDFIG = answer
    """
    try:
        sp = conceptcode.split("-")
        gameset = sp[0][1:]
        language = sp[1]

        ideas = []
        is_core = True
        for code_idea in sp[2].split("i")[1:]:
            idea = {"concepts": []} # TODO Missing core
            if is_core:
                idea['is_core'] = True
                is_core = False
            for code_concept in code_idea.split("c")[1:]:
                concept = code_concept.split("p")
                idea['concepts'].append({"id" : concept[0], "points": concept[1]})
            ideas.append(idea)
        answer = base64.b64decode(sp[3].encode("utf-8")).decode("utf-8")
        return json.dumps({"game" : {
            "set": gameset,
            "answer": answer,
            "language": language,
            "ideas": ideas,
        }})
    except:
        print("Something went wrong during the parsing of " + conceptcode)
        return None

def get_set():
    current_set = {
        0 : {'image': 'object.png', 'description': ['Object', 'Thing', 'Package']},
        1 : {'image': 'person.png', 'description': ['Person', 'Family', 'Group']},
        2 : {'image': 'female.png', 'description': ['Female', 'Woman', 'Wife', 'Feminine']},
        3 : {'image': 'male.png', 'description': ['Male', 'Man', 'Husband', 'Masculine']},
        4 : {'image': 'work.png', 'description': ['Work', 'Profession', 'Craft']},
        5 : {'image': 'recreation.png', 'description': ['Recreation', 'Sport', 'Activity']},
        6 : {'image': 'wildlife.png', 'description': ['Wildlife', 'Animal']},
        7 : {'image': 'flora.png', 'description': ['Flora', 'Nature', 'Plant']},
        8 : {'image': 'literature.png', 'description': ['Literature', 'Writing', 'Book']},
        9 : {'image': 'music.png', 'description': ['Music', 'Song', 'Note']},
        10: {'image': 'theater.png', 'description': ['Theater', 'Film', 'Camera']},
        11: {'image': 'arts.png', 'description': ['Arts', 'Scupture', 'Painting', 'Drawing', 'Comics']},
        12: {'image': 'television.png', 'description': ['Television', 'Broadcast', 'Series']},
        13: {'image': 'title.png', 'description': ['Title', 'Brand', 'Name']},
        14: {'image': 'idea.png', 'description': ['Idea', 'Thought', 'Concept']},
        15: {'image': 'expression.png', 'description': ['Expression', 'Quote', 'Speak', 'Word']},
        16: {'image': 'location.png', 'description': ['Location', 'Country', 'Flag']},
        17: {'image': 'building.png', 'description': ['Building', 'Construction', 'City']},
        18: {'image': 'date.png', 'description': ['Date', 'Event', 'Daytime']},
        19: {'image': 'holidays.png', 'description': ['Holidays', 'Birthday', 'Celebration']},
        20: {'image': 'watercraft.png', 'description': ['Watercraft', 'Maritime', 'Swim']},
        21: {'image': 'fly.png', 'description': ['Airborne vehicle', 'Airline', 'Fly']},
        22: {'image': 'car.png', 'description': ['Land vehicle', 'Car', 'Ride']},
        23: {'image': 'tools.png', 'description': ['Tools', 'Construction']},
        24: {'image': 'games.png', 'description': ['Games', 'Toys', 'Youth']},
        25: {'image': 'clothing.png', 'description': ['Clothing', 'Accessories', 'Costume']},
        26: {'image': 'food.png', 'description': ['Food', 'Nutrition', 'Edible']},
        27: {'image': 'home.png', 'description': ['Home', 'Interior', 'Domestic']},
        28: {'image': 'reality.png', 'description': ['Reality', 'History']},
        29: {'image': 'fictional.png', 'description': ['Fictional', 'Imaginary', 'Wish']},
        30: {'image': 'baby.png', 'description': ['Baby', 'Child', 'Young', 'New']},
        31: {'image': 'adult.png', 'description': ['Adult', 'Old', 'Ancient', 'Past']},
        32: {'image': 'slow.png', 'description': ['Slow', 'Lengthy', 'Turtle']},
        33: {'image': 'fast.png', 'description': ['Fast', 'Lively', 'Hare']},
        34: {'image': 'defense.png', 'description': ['Defense', 'Protection', 'Wall']},
        35: {'image': 'conflict.png', 'description': ['Conflict', 'Weapon', 'Fight']},
        36: {'image': 'life.png', 'description': ['Life', 'Heart', 'Love']},
        37: {'image': 'death.png', 'description': ['Death', 'Evil', 'Disease']},
        38: {'image': 'joyous.png', 'description': ['Joyous', 'Positive']},
        39: {'image': 'sad.png', 'description': ['Sad', 'Negative']},
        40: {'image': 'electronics.png', 'description': ['Electronics', 'Computer']},
        41: {'image': 'mechanical.png', 'description': ['Mechanical', 'Industrial']},
        42: {'image': 'money.png', 'description': ['Money', 'Rich', 'Expensive']},
        43: {'image': 'time.png', 'description': ['Time', 'Duration']},
        44: {'image': 'religion.png', 'description': ['Religion', 'Myth', 'Belief']},
        45: {'image': 'power.png', 'description': ['Power', 'Politics']},
        46: {'image': 'science.png', 'description': ['Science', 'Mathematics', 'Chemistry']},
        47: {'image': 'medical.png', 'description': ['Medical', 'Drug', 'Cure']},
        48: {'image': 'head.png', 'description': ['Head', 'Face']},
        49: {'image': 'arm.png', 'description': ['Arm', 'Hand']},
        50: {'image': 'torso.png', 'description': ['Torso', 'Stomach']},
        51: {'image': 'leg.png', 'description': ['Leg', 'Foot']},
        52: {'image': 'ear.png', 'description': ['Ear', 'Sound', 'Hear']},
        53: {'image': 'nose.png', 'description': ['Nose', 'Odor', 'Smell']},
        54: {'image': 'eye.png', 'description': ['Eye', 'View', 'Watch']},
        55: {'image': 'mouth.png', 'description': ['Mouth', 'Flavor', 'Eat']},
        56: {'image': 'cloud.png', 'description': ['Cloud', 'Rain', 'Snow', 'Cold']},
        57: {'image': 'lightning.png', 'description': ['Lightning', 'Electricity', 'Storm', 'Anger']},
        58: {'image': 'night.png', 'description': ['Night', 'Evening', 'Moon']},
        59: {'image': 'sun.png', 'description': ['Sun', 'Heat', 'Light', 'Daytime']},
        60: {'image': 'air.png', 'description': ['Air', 'Wind', 'Blow']},
        61: {'image': 'earth.png', 'description': ['Earth', 'Dirt', 'Grow']},
        62: {'image': 'rock.png', 'description': ['Rock', 'Mineral', 'Hard']},
        63: {'image': 'wood.png', 'description': ['Wood']},
        64: {'image': 'metal.png', 'description': ['Metal']},
        65: {'image': 'fabric.png', 'description': ['Fabric']},
        66: {'image': 'plastic.png', 'description': ['Plastic', 'Rubber']},
        67: {'image': 'paper.png', 'description': ['Paper', 'Sheet']},
        68: {'image': 'opposed.png', 'description': ['Opposed', 'Contrary', 'Inverse']},
        69: {'image': 'break.png', 'description': ['Break', 'Separate', 'Half']},
        70: {'image': 'fragment.png', 'description': ['Fragment', 'Multitude', 'Powder']},
        71: {'image': 'part.png', 'description': ['Part', 'Bit', 'Piece']},
        72: {'image': 'inside.png', 'description': ['Inside', 'Internal']},
        72: {'image': 'grid.png', 'description': ['Grid', 'Network', 'Prison']},
        73: {'image': 'zero.png', 'description': ['Zero', 'Nothing', 'Null']},
        74: {'image': 'unity.png', 'description': ['Unity', 'One']},
        75: {'image': 'line.png', 'description': ['Straight line', 'Smooth', 'Rise']},
        76: {'image': 'curve.png', 'description': ['Curve', 'Arc', 'Rounded']},
        77: {'image': 'cross.png', 'description': ['Cross', 'Intersection', 'Addition']},
        78: {'image': 'brokenline.png', 'description': ['Broken line', 'Sharp', 'Uneven']},
        79: {'image': 'spiral.png', 'description': ['Spiral', 'Intoxication', 'Madness', 'Coil']},
        80: {'image': 'sinusoidal.png', 'description': ['Sinusoidal', 'Ripple', 'Hair']},
        81: {'image': 'ring.png', 'description': ['Ring', 'cycle']},
        82: {'image': 'circle.png', 'description': ['Circle', 'Button']},
        83: {'image': 'triangle.png', 'description': ['Triange']},
        84: {'image': 'star.png', 'description': ['Star']},
        85: {'image': 'rectangle.png', 'description': ['Rectangle', 'Square']},
        86: {'image': 'flat.png', 'description': ['Flat']},
        87: {'image': 'cube.png', 'description': ['Cube', 'Brick']},
        88: {'image': 'sphere.png', 'description': ['Sphere']},
        89: {'image': 'pyramid.png', 'description': ['Pyramid']},
        90: {'image': 'cylinder.png', 'description': ['Cylinder']},
        91: {'image': 'cone.png', 'description': ['Cone']},
        92: {'image': 'hollow.png', 'description': ['Hollow', 'Hole', 'Pierced']},
        93: {'image': 'tall.png', 'description': ['Tall', 'Greater', 'High']},
        94: {'image': 'small.png', 'description': ['Small', 'Lower', 'Below']},
        95: {'image': 'huge.png', 'description': ['Huge', 'Wider', 'Longer']},
        96: {'image': 'skinny.png', 'description': ['Skinny', 'Closer', 'Brief']},
        97: {'image': 'top.png', 'description': ['Top', 'Up', 'Mount']},
        98: {'image': 'low.png', 'description': ['Low', 'Down', 'Under']},
        99: {'image': 'left.png', 'description': ['Left', 'First', 'Before']},
        100: {'image': 'right.png', 'description': ['Right', 'End', 'After']},
        101: {'image': 'turn.png', 'description': ['Turn', 'Surround', 'Cycle']},
        102: {'image': 'use.png', 'description': ['Use', 'Activate', 'Verb']},
        103: {'image': 'red.png', 'description': ['Red']},
        104: {'image': 'orange.png', 'description': ['Orange']},
        105: {'image': 'yellow.png', 'description': ['Yellow']},
        106: {'image': 'green.png', 'description': ['Green']},
        107: {'image': 'blue.png', 'description': ['Blue']},
        108: {'image': 'purple.png', 'description': ['Purple']},
        109: {'image': 'pink.png', 'description': ['Pink']},
        110: {'image': 'brown.png', 'description': ['Brown']},
        111: {'image': 'black.png', 'description': ['Black']},
        112: {'image': 'gray.png', 'description': ['Gray']},
        113: {'image': 'white.png', 'description': ['White']},
        114: {'image': 'clear.png', 'description': ['Clear', 'Invisible']}
    }
    return current_set
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
def creation():
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
        0 : {'image': 'object.svg', 'description': ['Object', 'Thing', 'Package']},
        1 : {'image': 'person.svg', 'description': ['Person', 'Family', 'Group']},
        2 : {'image': 'female.svg', 'description': ['Female', 'Woman', 'Wife', 'Feminine']},
        3 : {'image': 'male.svg', 'description': ['Male', 'Man', 'Husband', 'Masculine']},
        4 : {'image': 'work.svg', 'description': ['Work', 'Profession', 'Craft']},
        5 : {'image': 'recreation.svg', 'description': ['Recreation', 'Sport', 'Activity']},
        6 : {'image': 'wildlife.svg', 'description': ['Wildlife', 'Animal']},
        7 : {'image': 'flora.svg', 'description': ['Flora', 'Nature', 'Plant']},
        8 : {'image': 'literature.svg', 'description': ['Literature', 'Writing', 'Book']},
        9 : {'image': 'music.svg', 'description': ['Music', 'Song', 'Note']},
        10: {'image': 'theater.svg', 'description': ['Theater', 'Film', 'Camera']},
        # 11: {'image': 'arts.svg', 'description': ['Arts', 'Scupture', 'Painting', 'Drawing', 'Comics']},
        # 12: {'image': 'television.svg', 'description': ['Television', 'Broadcast', 'Series']},
        # 13: {'image': 'title.svg', 'description': ['Title', 'Brand', 'Name']},
        # 14: {'image': 'idea.svg', 'description': ['Idea', 'Thought', 'Concept']},
        # 15: {'image': 'expression.svg', 'description': ['Expression', 'Quote', 'Speak', 'Word']},
        # 16: {'image': 'location.svg', 'description': ['Location', 'Country', 'Flag']},
        # 17: {'image': 'building.svg', 'description': ['Building', 'Construction', 'City']},
        # 18: {'image': 'date.svg', 'description': ['Date', 'Event', 'Daytime']},
        # 19: {'image': 'holidays.svg', 'description': ['Holidays', 'Birthday', 'Celebration']},
        # 20: {'image': 'watercraft.svg', 'description': ['Watercraft', 'Maritime', 'Swim']},
        # 21: {'image': 'fly.svg', 'description': ['Airborne vehicle', 'Airline', 'Fly']},
        # 22: {'image': 'car.svg', 'description': ['Land vehicle', 'Car', 'Ride']},
        # 23: {'image': 'tools.svg', 'description': ['Tools', 'Construction']},
        # 24: {'image': 'games.svg', 'description': ['Games', 'Toys', 'Youth']},
        # 25: {'image': 'clothing.svg', 'description': ['Clothing', 'Accessories', 'Costume']},
        # 26: {'image': 'food.svg', 'description': ['Food', 'Nutrition', 'Edible']},
        # 27: {'image': 'reality.svg', 'description': ['Reality', 'History']},
        # 28: {'image': 'home.svg', 'description': ['Home', 'Interior', 'Domestic']},
        # 29: {'image': 'fictional.svg', 'description': ['Fictional', 'Imaginary', 'Wish']},
        # 30: {'image': 'baby.svg', 'description': ['Baby', 'Child', 'Young', 'New']},
        # 31: {'image': 'adult.svg', 'description': ['Adult', 'Old', 'Ancient', 'Past']},
        # 32: {'image': 'slow.svg', 'description': ['Slow', 'Lengthy', 'Turtle']},
        # 33: {'image': 'fast.svg', 'description': ['Fast', 'Lively', 'Hare']},
        # 34: {'image': 'defense.svg', 'description': ['Defense', 'Protection', 'Wall']},
        # 35: {'image': 'conflict.svg', 'description': ['Conflict', 'Weapon', 'Fight']},
        # 36: {'image': 'life.svg', 'description': ['Life', 'Heart', 'Love']},
        # 37: {'image': 'death.svg', 'description': ['Death', 'Evil', 'Disease']},
        # 38: {'image': 'joyous.svg', 'description': ['Joyous', 'Positive']},
        # 39: {'image': 'sad.svg', 'description': ['Sad', 'Negative']},
        # 40: {'image': 'electronics.svg', 'description': ['Electronics', 'Computer']},
        # 41: {'image': 'mechanical.svg', 'description': ['Mechanical', 'Industrial']},
        # 42: {'image': 'money.svg', 'description': ['Money', 'Rich', 'Expensive']},
        # 43: {'image': 'time.svg', 'description': ['Time', 'Duration']},
        # 44: {'image': 'religion.svg', 'description': ['Religion', 'Myth', 'Belief']},
        # 45: {'image': 'power.svg', 'description': ['Power', 'Politics']},
        # 46: {'image': 'science.svg', 'description': ['Science', 'Mathematics', 'Chemistry']},
        # 47: {'image': 'medical.svg', 'description': ['Medical', 'Drug', 'Cure']},
        # 48: {'image': 'head.svg', 'description': ['Head', 'Face']},
        # 49: {'image': 'arm.svg', 'description': ['Arm', 'Hand']},
        # 50: {'image': 'torso.svg', 'description': ['Torso', 'Stomach']},
        # 51: {'image': 'leg.svg', 'description': ['Leg', 'Foot']},
        # 52: {'image': 'ear.svg', 'description': ['Ear', 'Sound', 'Hear']},
        # 53: {'image': 'nose.svg', 'description': ['Nose', 'Odor', 'Smell']},
        # 54: {'image': 'eye.svg', 'description': ['Eye', 'View', 'Watch']},
        # 55: {'image': 'mouth.svg', 'description': ['Mouth', 'Flavor', 'Eat']},
        # 56: {'image': 'cloud.svg', 'description': ['Cloud', 'Rain', 'Snow', 'Cold']},
        # 57: {'image': 'lightning.svg', 'description': ['Lightning', 'Electricity', 'Storm', 'Anger']},
        # 58: {'image': 'night.svg', 'description': ['Night', 'Evening', 'Moon']},
        # 59: {'image': 'sun.svg', 'description': ['Sun', 'Heat', 'Light', 'Daytime']},
        # 60: {'image': 'air.svg', 'description': ['Air', 'Wind', 'Blow']},
        # 61: {'image': 'earth.svg', 'description': ['Earth', 'Dirt', 'Grow']},
        # 62: {'image': 'rock.svg', 'description': ['Rock', 'Mineral', 'Hard']},
        # 63: {'image': 'wood.svg', 'description': ['Wood']},
        # 64: {'image': 'metal.svg', 'description': ['Metal']},
        # 65: {'image': 'fabric.svg', 'description': ['Fabric']},
        # 66: {'image': 'plastic.svg', 'description': ['Plastic', 'Rubber']},
        # 67: {'image': 'paper.svg', 'description': ['Paper', 'Sheet']},
        # 68: {'image': 'opposed.svg', 'description': ['Opposed', 'Contrary', 'Inverse']},
        # 69: {'image': 'break.svg', 'description': ['Break', 'Separate', 'Half']},
        # 70: {'image': 'fragment.svg', 'description': ['Fragment', 'Multitude', 'Powder']},
        # 71: {'image': 'part.svg', 'description': ['Part', 'Bit', 'Piece']},
        # 72: {'image': 'inside.svg', 'description': ['Inside', 'Internal']},
        # 72: {'image': 'grid.svg', 'description': ['Grid', 'Network', 'Prison']},
        # 73: {'image': 'zero.svg', 'description': ['Zero', 'Nothing', 'Null']},
        # 74: {'image': 'unity.svg', 'description': ['Unity', 'One']},
        # 75: {'image': 'line.svg', 'description': ['Straight line', 'Smooth', 'Rise']},
        # 76: {'image': 'curve.svg', 'description': ['Curve', 'Arc', 'Rounded']},
        # 77: {'image': 'cross.svg', 'description': ['Cross', 'Intersection', 'Addition']},
        # 78: {'image': 'brokenline.svg', 'description': ['Broken line', 'Sharp', 'Uneven']},
        # 79: {'image': 'spiral.svg', 'description': ['Spiral', 'Intoxication', 'Madness', 'Coil']},
        # 80: {'image': 'sinusoidal.svg', 'description': ['Sinusoidal', 'Ripple', 'Hair']},
        # 81: {'image': 'ring.svg', 'description': ['Ring', 'cycle']},
        # 82: {'image': 'circle.svg', 'description': ['Circle', 'Button']},
        # 83: {'image': 'triangle.svg', 'description': ['Triange']},
        # 84: {'image': 'star.svg', 'description': ['Star']},
        # 85: {'image': 'rectangle.svg', 'description': ['Rectangle', 'Square']},
        # 86: {'image': 'flat.svg', 'description': ['Flat']},
        # 87: {'image': 'cube.svg', 'description': ['Cube', 'Brick']},
        # 88: {'image': 'sphere.svg', 'description': ['Sphere']},
        # 89: {'image': 'pyramid.svg', 'description': ['Pyramid']},
        # 90: {'image': 'cylinder.svg', 'description': ['Cylinder']},
        # 91: {'image': 'cone.svg', 'description': ['Cone']},
        # 92: {'image': 'hollow.svg', 'description': ['Hollow', 'Hole', 'Pierced']},
        # 93: {'image': 'tall.svg', 'description': ['Tall', 'Greater', 'High']},
        # 94: {'image': 'small.svg', 'description': ['Small', 'Lower', 'Below']},
        # 95: {'image': 'huge.svg', 'description': ['Huge', 'Wider', 'Longer']},
        # 96: {'image': 'skinny.svg', 'description': ['Skinny', 'Closer', 'Brief']},
        # 97: {'image': 'top.svg', 'description': ['Top', 'Up', 'Mount']},
        # 98: {'image': 'low.svg', 'description': ['Low', 'Down', 'Under']},
        # 99: {'image': 'left.svg', 'description': ['Left', 'First', 'Before']},
        # 100: {'image': 'right.svg', 'description': ['Right', 'End', 'After']},
        # 101: {'image': 'turn.svg', 'description': ['Turn', 'Surround', 'Cycle']},
        # 102: {'image': 'use.svg', 'description': ['Use', 'Activate', 'Verb']},
        # 103: {'image': 'red.svg', 'description': ['Red']},
        # 104: {'image': 'orange.svg', 'description': ['Orange']},
        # 105: {'image': 'yellow.svg', 'description': ['Yellow']},
        # 106: {'image': 'green.svg', 'description': ['Green']},
        # 107: {'image': 'blue.svg', 'description': ['Blue']},
        # 108: {'image': 'purple.svg', 'description': ['Purple']},
        # 109: {'image': 'pink.svg', 'description': ['Pink']},
        # 110: {'image': 'brown.svg', 'description': ['Brown']},
        # 111: {'image': 'black.svg', 'description': ['Black']},
        # 112: {'image': 'gray.svg', 'description': ['Gray']},
        # 113: {'image': 'white.svg', 'description': ['White']},
        # 114: {'image': 'clear.svg', 'description': ['Clear', 'Invisible']}
    }
    return current_set
# -*- coding: utf-8 -*-
"""Game models."""
import datetime as dt

from enum import Enum
from concept.database import Column, PkModel, db, reference_col, relationship

class Concept():
    """Original set of concepts."""

    id = -1

    def __init__(self, id) -> None:
        self.id = id


class Idea():
    """An idea. It represents what the other player must guess. It is a sum of concepts."""

    concepts = []

    def __init__(self, set, answer, language, concepts) -> None:
        self.set = set
        self.answer = answer
        self.language = language
        self.concepts = concepts

"""
TODO This should be moved somewhere else, like inside a configuration file
"""
class DefaultConceptSet(Enum):
    OBJECT = (0, ['Object', 'Thing', 'Package'], 'image/object.png') # How to handle languages?
    # TODO Add remaining concepts
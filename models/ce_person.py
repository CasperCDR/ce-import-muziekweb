"""Trompa Person model
"""

from dataclasses import dataclass
from datetime import date
from . import CE_BaseModel
from . import Person

@dataclass
class CE_Person(Person, CE_BaseModel):
    """
    Trompa Person model

    Inherits from schema.org Person
    """
    pass

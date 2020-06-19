"""Trompa Person model
"""

from dataclasses import dataclass
from . import CE_BaseModel, Person

@dataclass
class CE_Person(Person, CE_BaseModel):
    """
    Trompa Person model

    Inherits from schema.org Person
    """
    pass

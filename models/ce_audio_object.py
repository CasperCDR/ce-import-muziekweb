"""Trompa AudioObject model
"""

from dataclasses import dataclass
from . import CE_BaseModel, AudioObject

@dataclass
class CE_AudioObject(AudioObject, CE_BaseModel):
    """
    Trompa AudioObject model

    Inherits from schema.org AudioObject
    """

    def __init__(self, identifier: str, name: str, url: str, contributor: str, creator: str):
        super().__init__(identifier, name, url, contributor, creator)
        self.format = "audio/aac"

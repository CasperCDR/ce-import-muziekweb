"""Trompa MusicAlbum model
"""

from dataclasses import dataclass
from . import CE_BaseModel, MusicAlbum

@dataclass
class CE_MusicAlbum(MusicAlbum, CE_BaseModel):
    """
    Trompa MusicAlbum model

    Inherits from schema.org MusicAlbum
    """
    pass

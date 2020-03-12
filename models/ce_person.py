"""Trompa Person model
"""

from dataclasses import dataclass
from datetime import date
from . import Person

@dataclass
class CE_Person(Person):
    """
    Trompa Person model

    Inherits from schema.org Person

    Attributes
    ----------
    contributor
        Text (Mandatory)
        A person, an organization, or a service responsible for contributing
        the artist to the web resource. This can be either a name or a base
        URL.
    source
        URL
        Url refering to the source
    coverage
        Text
        The spatial or temporal topic of the resource, the spatial
        applicability of the resource, or the jurisdiction under which the
        resource is relevant.
    creator: String!
        Text (Mandatory)
        The person, organization or service who created the thing the web
        resource is about.
    date
        _Neo4jDate
        A point in time associated with an event in the lifecycle of the
        resource. Accepts a date type, year(int) or list with [year, month,
        date] where month and date are optional.
    format
        Text (Mandatory)
        Format the resource is represented in.
    language
        AvailableLanguage
        The language the metadata is written in. Currently supported languages
        are en,es,ca,nl,de,fr.
    publisher
        Text
        The person, organization or service responsible for making the artist
        information available.
    relation
        Text
        A related resource. Any web resource can be used as a relation.
    rights
        Text
        The applicable rights for the resource.
    subject
        Text
        Resource type of the referenced object.
    title
        Text
        Title for the resource.
    _type
        Text
        The String scalar type represents textual data, represented as UTF-8
        character sequences. The String type is most often used by GraphQL to
        represent free-form human-readable text.
    _searchScore
        Float
        The Float scalar type represents signed double-precision fractional
        values as specified by IEEE 754.
    """

    def __init__(self, identifier: str, name: str, url: str, contributor: str, creator: str):
        self.identifier = identifier
        self.name = name
        self.title = name
        self.url = url
        self.contributor = contributor
        self.source = url
        self.creator = creator
        self.date = date.today()

    source: str = None
    contributor: str = None
    creator: str = None
    coverage: str = None
    date = None
    format: str = "text/html"
    language: str = "en"
    publisher: str = None
    relation: str = None
    rights: str = None
    subject: str = None
    title: str = None
    _type: str = None
    _searchScore: float = None

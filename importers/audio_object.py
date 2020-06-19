"""
Muziekweb artist importer
"""
import json
import trompace as ce

from datetime import datetime, date
from SPARQLWrapper import SPARQLWrapper, JSON
from trompace.connection import submit_query
from trompace.mutations.person import mutation_update_artist, mutation_create_artist
from trompace_local import GLOBAL_CONTRIBUTOR, GLOBAL_IMPORTER_REPO, GLOBAL_PUBLISHER, lookupIdentifier

from models import CE_AudioObject

async def import_tracks(keys: list):
    """
    Imports audio fragments from Muziekweb for all given keys into the Trompa CE.
    """
    for key in keys:
        print(f"Retrieving release info with key {key} from Muziekweb")
        # Get data from Muziekweb
        tracks = await get_mw_audio(key)

        if tracks is None:
            print(f"No data received for {key}")
            continue

        # Loop the tracks on the release to add all references to the 30 seconds music fragment
        for track in tracks:

            track.identifier = await lookupIdentifier("AudioObject", track.source)

            if track.identifier is not None:
                print(f"Updating record {track.identifier} in Trompa CE", end="")
                response = await ce.connection.submit_query(mutation_update_artist(
                    identifier=track.identifier,
                    artist_name=track.name,
                    publisher=track.publisher,
                    contributor=track.contributor,
                    creator=track.creator,
                    source=track.source,
                    description=track.description,
                    language=track.language,
                    coverage=None,
                    #formatin="text/html",
                    date=date.today(),
                    disambiguatingDescription=track.disambiguatingDescription,
                    relation=track.relatedTo,
                    _type=None,
                    _searchScore=None,
                    additionalType=track.additionalType,
                    alternateName=track.alternateName,
                    image=track.image,
                    sameAs=track.sameAs,
                    url=track.url,
                    additionalName=track.additionalName,
                    award=track.award,
                    birthDate=track.birthDate,
                    deathDate=track.deathDate,
                    familyName=track.familyName,
                    gender=track.gender,
                    givenName=track.givenName,
                    honorificPrefix=track.honorificPrefix,
                    honorificSuffix=track.honorificSuffix,
                    jobTitle=track.jobTitle,
                    knowsLanguage=track.knowsLanguage
                ))
                track.identifier = response["data"]["UpdatePerson"]["identifier"]
            else:
                print("Inserting new record in Trompa CE", end="")
                response = await ce.connection.submit_query(mutation_create_artist(
                    artist_name=track.name,
                    publisher=track.publisher,
                    contributor=track.contributor,
                    creator=track.creator,
                    source=track.source,
                    description=track.description,
                    language=track.language,
                    coverage=None,
                    #formatin="text/html",
                    date=date.today(),
                    disambiguatingDescription=track.disambiguatingDescription,
                    relation=track.relatedTo,
                    _type=None,
                    _searchScore=None,
                    additionalType=track.additionalType,
                    alternateName=track.alternateName,
                    image=track.image,
                    sameAs=track.sameAs,
                    url=track.url,
                    additionalName=track.additionalName,
                    award=track.award,
                    birthDate=track.birthDate,
                    deathDate=track.deathDate,
                    familyName=track.familyName,
                    gender=track.gender,
                    givenName=track.givenName,
                    honorificPrefix=track.honorificPrefix,
                    honorificSuffix=track.honorificSuffix,
                    jobTitle=track.jobTitle,
                    knowsLanguage=track.knowsLanguage
                ))
                track.identifier = response["data"]["CreatePerson"]["identifier"]

            if track.identifier is None:
                print(" - failed.")
            else:
                print(" - success.")

    print("Importing artists done.")


async def get_mw_audio(key: str) -> [CE_AudioObject]:
    sparql = SPARQLWrapper("https://api.data.muziekweb.nl/datasets/muziekweborganization/Muziekweb/services/Muziekweb/sparql")
    sparql.setReturnFormat(JSON)
    qry = f"""PREFIX schema: <http://schema.org/>
    PREFIX vocab: <https://data.muziekweb.nl/vocab/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    select ?url ?name ?birthYear ?deathYear where {{
        BIND(<https://data.muziekweb.nl/Link/{key}> as ?url)
        ?url vocab:beginYear ?birthYear;
            vocab:endYear ?deathYear;
            rdfs:label ?name.
    }}"""
    sparql.setQuery(qry)

    result = sparql.query().convert()["results"]["bindings"]

    if len(result) > 0:
        # Now extract the audio links from the Muziekweb data

        person = CE_AudioObject(
            identifier = None,
            name = result[0]["name"]["value"],
            url = result[0]["url"]["value"],
            contributor = GLOBAL_CONTRIBUTOR,
            creator = GLOBAL_IMPORTER_REPO,
        )

        person.publisher = GLOBAL_PUBLISHER
        person.description = None
        person.birthDate = result[0]["birthYear"]["value"]
        person.deathDate = result[0]["deathYear"]["value"]

        return person

    return None

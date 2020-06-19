"""
Muziekweb album importer
"""
import json
import trompace as ce

from datetime import datetime, date
from SPARQLWrapper import SPARQLWrapper, JSON
from trompace.connection import submit_query
from trompace.mutations.person import mutation_update_artist, mutation_create_artist
from trompace_local import GLOBAL_CONTRIBUTOR, GLOBAL_IMPORTER_REPO, GLOBAL_PUBLISHER, lookupIdentifier

from models import CE_MusicAlbum

async def import_album(keys: list):
    """
    Imports albums from Muziekweb for all given keys into the Trompa CE.
    """
    for key in keys:
        print(f"Retrieving album with key {key} from Muziekweb")
        # Get data from Muziekweb
        album = await get_mw_album(key)

        if album is None:
            print(f"No data received for {key}")
            continue

        album.identifier = await lookupIdentifier("MusicAlbum", album.source)

        if album.identifier is not None:
            print(f"Updating record {album.identifier} in Trompa CE", end="")
            response = await ce.connection.submit_query(mutation_update_artist(
                identifier=album.identifier,
                artist_name=album.name,
                publisher=album.publisher,
                contributor=album.contributor,
                creator=album.creator,
                source=album.source,
                description=album.description,
                language=album.language,
                coverage=None,
                #formatin="text/html",
                date=date.today(),
                disambiguatingDescription=album.disambiguatingDescription,
                relation=album.relatedTo,
                _type=None,
                _searchScore=None,
                additionalType=album.additionalType,
                alternateName=album.alternateName,
                image=album.image,
                sameAs=album.sameAs,
                url=album.url,
                additionalName=album.additionalName,
                award=album.award,
                birthDate=album.birthDate,
                deathDate=album.deathDate,
                familyName=album.familyName,
                gender=album.gender,
                givenName=album.givenName,
                honorificPrefix=album.honorificPrefix,
                honorificSuffix=album.honorificSuffix,
                jobTitle=album.jobTitle,
                knowsLanguage=album.knowsLanguage
            ))
            album.identifier = response["data"]["UpdatePerson"]["identifier"]
        else:
            print("Inserting new record in Trompa CE", end="")
            response = await ce.connection.submit_query(mutation_create_artist(
                artist_name=album.name,
                publisher=album.publisher,
                contributor=album.contributor,
                creator=album.creator,
                source=album.source,
                description=album.description,
                language=album.language,
                coverage=None,
                #formatin="text/html",
                date=date.today(),
                disambiguatingDescription=album.disambiguatingDescription,
                relation=album.relatedTo,
                _type=None,
                _searchScore=None,
                additionalType=album.additionalType,
                alternateName=album.alternateName,
                image=album.image,
                sameAs=album.sameAs,
                url=album.url,
                additionalName=album.additionalName,
                award=album.award,
                birthDate=album.birthDate,
                deathDate=album.deathDate,
                familyName=album.familyName,
                gender=album.gender,
                givenName=album.givenName,
                honorificPrefix=album.honorificPrefix,
                honorificSuffix=album.honorificSuffix,
                jobTitle=album.jobTitle,
                knowsLanguage=album.knowsLanguage
            ))
            album.identifier = response["data"]["CreatePerson"]["identifier"]

        if album.identifier is None:
            print(" - failed.")
        else:
            print(" - success.")

    print("Importing albums done.")


async def get_mw_album(key: str) -> CE_MusicAlbum:
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
        # Now get Muziekweb data
        album = CE_MusicAlbum(
            identifier = None,
            name = result[0]["name"]["value"],
            url = result[0]["url"]["value"],
            contributor = GLOBAL_CONTRIBUTOR,
            creator = GLOBAL_IMPORTER_REPO,
        )

        album.publisher = GLOBAL_PUBLISHER
        album.description = None
        album.birthDate = result[0]["birthYear"]["value"]
        album.deathDate = result[0]["deathYear"]["value"]

        return album

    return None

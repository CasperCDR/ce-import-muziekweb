"""
Local functions to select data from the Trompa CE.
"""
import trompace as ce
from trompace.connection import submit_query


async def queryFor(dataType, field, value):
    """
    Queries CE for objects by type and identifying field value.
    """
    search_query = f"""
    query {{
        {dataType}({field} : \"{value}\") {{
            identifier
            name
            source
            contributor
            publisher
        }}
    }}
    """
    resultset = await ce.connection.submit_query(search_query)

    return resultset["data"][dataType]


async def lookupIdentifier(dataType, source):
    """
    Lookup the identifier by the source link. It returns the first
    identifier it finds for the given source.
    """
    objects = await queryFor(dataType, "source", source)

    if isinstance(objects, list) and len(objects) > 0:
        return objects[0]["identifier"]

    return None

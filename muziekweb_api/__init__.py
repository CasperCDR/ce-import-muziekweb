"""
Basic use of the Muziekweb REST API.
"""
import urllib.request, getpass
from xml.dom import minidom

"""
Constants for Muziekweb API
"""
MW_API_HOST = "http://api.cdr.nl:8080"

_api_activated = False

def set_api_account(user, password):
    global _api_activated

    passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, MW_API_HOST, user, password)
    authhandler = urllib.request.HTTPBasicAuthHandler(passman)
    opener = urllib.request.build_opener(authhandler)
    urllib.request.install_opener(opener)

    _api_activated = True


def get_album_information(key: str):
    global _api_activated

    if _api_activated:
        # Use the Muziekweb API to retrieve all the tracks on the album
        response  = urllib.request.urlopen(f"{MW_API_HOST}/v2/search/albumInformation.xml?albumID={key}")
        body = response.read()

        if len(body) > 0:
            # Return the xml as object
            return minidom.parseString(body)

    return None

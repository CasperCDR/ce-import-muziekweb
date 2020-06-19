#!/usr/bin/env python3
"""
Trompa data importer for Muziekweb catalog.


Copyright 2019, C. Karreman
Licensed under GPLv3.
"""
import os
import argparse
import asyncio
import trompace as ce

from trompace import config
from importers import import_artist, import_album

# Environment settings (defaults)
trompa_ce_host = os.environ["CE_HOST"] if "CE_HOST" in os.environ else "http://localhost:4000"


# Construct the argument parser and parse the arguments
main_parser = argparse.ArgumentParser(description="Input data options:")
main_parser.add_argument("-a", dest="artist", required=False, help="Muziekweb performer_id or input file with Muziekweb performer identifiers.")
main_parser.add_argument("-r", dest="release", required=False, help="Muziekweb album_id or input file with Muziekweb albums release identifiers.")

# Trompa CE
main_parser.add_argument("-ce", dest="ce_host", required=False, help="Trompa CE host.")
#main_parser.add_argument("-u", dest="user", required=False, help="Database username.")
#main_parser.add_argument("-p", dest="password", required=False, help="User password.")

# Muziekweb API
main_parser.add_argument("-mwu", dest="mw_api_user", required=False, help="The username for the Muziekweb API.")
main_parser.add_argument("-mwp", dest="mw_api_pass", required=False, help="The password for the Muziekweb API.")


# Startup defaults or parameterized values
args = main_parser.parse_args()
# Import options
source_artist = None if args.artist is None else args.artist.strip(" \n\t\"")
source_release = None if args.release is None else args.release.strip(" \n\t\"")
source_track = None if args.track is None else args.track.strip(" \n\t\"")

# Trompa CE
trompa_ce_host = trompa_ce_host if args.ce_host is None else args.ce_host

# Muziekweb API
mw_api_user = None if args.mw_api_user is None else args.mw_api_user
mw_api_pass = None if args.mw_api_pass is None else args.mw_api_pass


def readKeys(input: str) -> [str]:
    if os.path.isfile(input):
        with open(input, "r") as f:
            keys = f.read().splitlines()
        return keys
    else:
        return [input]


if __name__ == "__main__":
    # Set the hostname where data data is imported
    _proto, _server = trompa_ce_host.split("://")
    ce.config.set_server(_server, (_proto == "https"))

    # Import Muziekweb artists into the Trompa CE
    asyncio.run(import_artist(readKeys(source_artist)))
    asyncio.run(import_album(readKeys(source_release)))

# Muziekweb data import for Trompa Contributor Environment

Muziekweb Rotterdam, the Netherlands

A python script that imports data from Muziekweb into the Trompa CE.

## Installation

For this application to run the Trompa CE Client is required. Download the
code from https://github.com/trompamusic/trompa-ce-client (for now the
"fix/remove-ce-host-setting-from-file" branch is required) and install the
package as python library by running the following commend in the root of the
package:

    python setup.py install

To install the package dependencies run:

    pip install requirements.txt

## Running the application

To import data from Muziekweb into the Trompa CE start the import-mw.py script
with the nescessary parameters. For example to import an artist identified by
the Muziekweb identifier 'M00000238467':

    python import-mw.py -a M00000238467

## License

```
Copyright 2020 Muziekweb

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

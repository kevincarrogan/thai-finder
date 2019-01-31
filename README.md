# Thai Finder

Finds Thai restaurants for those that like their food to be of top quality in the New York area.

## Usage

Finding a random restaurant to go to.

    $ curl --header "Content-Type: application/json" http://localhost:8000/restaurant/random/

    {
        "name": "AROY DEE THAI KITCHEN",
        "borough": "BRONX"
    }

## Installation

### Requirements

  * Python 2.7
  * pip

### Local

*Recommended to run in a [virtualenv](https://virtualenv.pypa.io/en/latest/)*

    $ pip install -r requirements.txt
    $ ./manage.py migrate

## Tests

Run tests using

    $ ./manage.py test

## Ideas

### Libraries

  - Django
  - bonobo

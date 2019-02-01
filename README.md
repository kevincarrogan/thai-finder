# Thai Finder

Finds Thai restaurants for those that like their food to be of top quality in the New York area.

## Usage

Finding a random restaurant to go to.

    $ curl --header "Content-Type: application/json" http://localhost:8000/restaurants/random/

    {
        "name": "AROY DEE THAI KITCHEN",
        "borough": "BRONX"
    }

Find top 10 restaurants by score filtered by cuisine and grade.

    $ curl --header "Content-Type: application/json" http://localhost:8000/restaurants/top10/?cuisine=thai&grade=B

    {
        "results": [
            {
                "name": "Thai Cottage",
                "borough": "BROOKLYN",
                "score": 10
            },
            {
                "name": "AROY DEE THAI KITCHEN",
                "borough": "BRONX",
                "score": 9
            },
            ...
        ]
    }


## Installation

### Requirements

  * Python 2.7
  * pip

### Local

*Recommended to run in a [virtualenv](https://virtualenv.pypa.io/en/latest/)*

    $ pip install -r requirements.txt
    $ ./manage.py migrate

### Import data

Data can be downloaded from https://data.cityofnewyork.us/api/views/43nn-pn8j/rows.csv?accessType=DOWNLOAD.

To import the data run:

    $ ./manage.py importrestaurantdata restaurants.csv

## Tests

Run tests using

    $ ./manage.py test

## Ideas

### Libraries

  - Django
  - bonobo

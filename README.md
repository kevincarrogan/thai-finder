# Thai Finder

Finds Thai restaurants for those that like their food to be of top quality in the New York area.

## Usage

Finding a random restaurant to go to.

    $ curl --header "Content-Type: application/json" https://thai-finder.herokuapp.com/restaurants/random/

    {
        "name": "AROY DEE THAI KITCHEN",
        "borough": "BRONX"
    }

Find top 10 restaurants by score filtered by cuisine and grade.

    $ curl --header "Content-Type: application/json" https://thai-finder.herokuapp.com/restaurants/top10/?cuisine=thai&grade=B

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

#### Querying the data

This data can be queried directly in the database.

For example, to find all Thai restaurants with a grade B rating ordered by score one could run:

    SELECT
        restaurants_restaurant.name, restaurants_borough.name
    FROM
        restaurants_restaurant
    INNER JOIN
        restaurants_borough ON restaurants_restaurant.borough_id = restaurants_borough.id
    INNER JOIN
        restaurants_cuisine ON restaurants_restaurant.cuisine_id = restaurants_cuisine.id
    WHERE
        restaurants_cuisine.name = 'Thai'
    ORDER BY
        restaurants_restaurant.score DESC

## Tests

Run tests using

    $ ./manage.py test

## Deployment

The project is configured to deploy to Heroku.

Before deploying the application the following steps need to be made:

    $ heroku config:set DISABLE_COLLECTSTATIC=1
    $ heroku config:set ENVIRONMENT='PROD'
    $ heroku config:set SECRET_KEY=<secret_key>
    $ heroku run "wget -O restaurants.csv https://data.cityofnewyork.us/api/views/43nn-pn8j/rows.csv\?accessType\=DOWNLOAD && python manage.py importrestaurantdata restaurants.csv"

## Schema

![Schema](schema.png)

The schema currently only breaks out the restaurant, cuisine and borough into separate tables/models.

In future this will probably expand to include additional data relevant to the restaurant.

The grade is also only recorded on the restaurant meaning that historical data isn't tracked. We may want to be able to model this and as such we would break this out into a separate table where we would record grades over time.

Currently the latest grade is recorded due to the current requirements for the project.

## Future work

Split out grade into a separate table tracking historical grade data. This would allow for more interesting queries of a restaurants quality over time.

Use an ETL library, such as bonobo, for importing the data. This should allow us to run the process in parallel (it's currently a long linear process) as well as allowing the way the data is imported to be changed easily.

Upgrade to Django 2.x. Depending on the nature of the project this may want to wait until a version of Django 2.x is in LTS or if the production envorinment no longer supports Python 2.7.

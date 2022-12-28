#!/usr/bin/env python

import csv
import json
import sqlalchemy


def csv_load():
    # connect to the database
    engine = sqlalchemy.create_engine("mysql+mysqldb://codetest:swordfish@localhost:3306/codetest", pool_recycle=3600, encoding='utf-8', echo=False)
    connection = engine.connect()
    metadata = sqlalchemy.schema.MetaData(engine)

    # make an ORM object to refer to the table
    get_examples = sqlalchemy.schema.Table(
        "examples", metadata, autoload=True, autoload_with=engine
    )
    get_places = sqlalchemy.schema.Table(
        "places", metadata, autoload=True, autoload_with=engine
    )
    get_peoples = sqlalchemy.schema.Table(
        "peoples", metadata, autoload=True, autoload_with=engine
    )

    with open("/data/input/example.csv") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            connection.execute(
                get_examples.insert().values(name=row[0])
            )

    with open("/data/input/places.csv") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            connection.execute(
                get_places.insert().values(city=row[0], county=row[1], country=row[2])
            )

    with open("/data/input/people.csv") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            connection.execute(
                get_peoples.insert().values(
                    given_name=row[0],
                    family_name=row[1],
                    date_of_birth=row[2],
                    place_of_birth=row[3],
                )
            )

def people_per_country_json():
    """output SQL-result to a JSON file"""

    engine = sqlalchemy.create_engine("mysql+mysqldb://codetest:swordfish@localhost:3306/codetest", pool_recycle=3600, encoding='utf-8', echo=True)
    connection = engine.connect()
    metadata = sqlalchemy.schema.MetaData(engine)

    #consider using ORM to join tables
    sql_statement = 'select country, count(1) num_of_people from places left join peoples on lower(place_of_birth) = lower(city) group by country'

    with open('/data/sample_output.json', 'w') as json_file:
        rows = connection.execute(sql_statement).fetchall()
        data_dict = {}
        for row in rows:
            data_dict[row[0]] = row[1]
        json.dump(data_dict, json_file, separators=(',', ':'))

def main():
    csv_load()
    people_per_country_json()


if __name__ == "__main__":
    main()

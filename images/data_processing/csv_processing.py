#!/usr/bin/env python

import csv
import json
import time
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, schema


def db_connect():
    # connect to the database
    engine = create_engine(
        "mysql://codetest:swordfish@database/codetest",
        pool_recycle=3600,
        encoding="utf-8",
        echo=False,
        pool_pre_ping=True,
    )

    try:
        print("MySQL Engine:", engine)
        time.sleep(10)
        engine.connect()
        print("Successfully connected to MySQL database!!!")
        return engine
    except SQLAlchemyError as err:
        error = str(err.__dict__["orig"])
        print(error)


def load_places(engine):
    metadata = schema.MetaData(engine)
    get_places = schema.Table("places", metadata, autoload=True, autoload_with=engine)
    try:
        with engine.connect() as connection:
            with open("/data/input/places.csv") as csv_file:
                reader = csv.reader(csv_file)
                next(reader)
                for row in reader:
                    connection.execute(
                        get_places.insert().values(
                            city=row[0], county=row[1], country=row[2]
                        )
                    )
    except:
        raise


def load_peoples(engine):
    metadata = schema.MetaData(engine)
    get_peoples = schema.Table("peoples", metadata, autoload=True, autoload_with=engine)
    try:
        with engine.connect() as connection:
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
    except:
        raise


def load_places_info(engine):
    sql = """
    insert into places_info (city, county, country)
    select city, county, country from places
    """
    try:
        with engine.connect() as connection:
            connection.execute(sql)
    except:
        raise


def load_peoples_info(engine):
    sql = """
    insert into peoples_info (given_name, family_name, date_of_birth, birth_place_id)
    select given_name, family_name, date_of_birth, pi.id
    from peoples p 
    left join places_info pi
    on lower(city) = lower(place_of_birth)
    """
    try:
        with engine.connect() as connection:
            connection.execute(sql)
    except:
        raise


def people_per_country_json(engine):
    try:
        with engine.connect() as connection:
            # consider using ORM to join tables
            sql_statement = """
            select country, count(1) num_of_people 
            from places_info pi1
            left join peoples_info pi2
            on birth_place_id = pi1.id 
            group by country
            order by num_of_people desc
            """

            with open("/data/sample_output.json", "w") as json_file:
                rows = connection.execute(sql_statement).fetchall()
                data_dict = {}
                for row in rows:
                    data_dict[row[0]] = row[1]
                json.dump(data_dict, json_file, separators=(",", ":"))
    except:
        raise


def main():
    engine = db_connect()
    load_places(engine)
    load_peoples(engine)
    load_places_info(engine)
    load_peoples_info(engine)
    people_per_country_json(engine)


if __name__ == "__main__":
    main()

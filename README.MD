# GotPhoto Data Engineering Challenge - Part 1
This repository contains code to load data into a `mysql` database from `CSV` files. peoples and places data is read from the files and transformed before loading into the database. It also enforces referential integrity (`PK-FK` realtionship) on the tables.

## Assumptions

- Data is cleaned. Thus, data cleaning and conversion is not required
- There exists no city with same name across different countries

## Steps

1. Build the docker image
    > `docker compose build`
2. Run the docker container for running `mysql:8.0` database. It will create the necessary schema and tables inside the database. Also, it will load the data into required tables.
	> `docker compose run data-processing`
3. Cleaning up the docker
    > `docker compose down`


# GotPhoto Data Engineering Challenge - Part 2
Refer *[gotphoto_de_dbt](https://github.com/reply2yds/gotphoto_de_dbt)* repository for transforming data using **DBT**
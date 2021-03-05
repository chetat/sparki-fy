# SPARKIFY PROJECT
## Purpose
The purpose of project is to have a database that collects songs and users' activities from sparkify music streaming app. The data collected from 
this app will be analyzed to understand what songs most users like listening to and improve users experiences by providing songs recommendation
tailored for each user.


## Database Schema and ETL pipeline
The database schema choosen for this project is the STAR schema. This choice was made because of the simplicity it offers in building facts and dimention tables. Through this schema, we'll be able to create a denormalized table from data extracted in json files or any json api source to make simple queries, and easily retrieve data for performing analysis and improving the user experience from the data gotten.

## Project Structure
- `data`: This directory contains the json files for logs and songs.
- `create_tables.py`: This file is used for creating new database and tables for the application.
- `etl.py`: This file handles the ETL process by reading and process data from files in the `data` directory and then insert
the data in the database.
- `sql_queries`: This file contains the various sql queries called in `create_tables.py` file.
- `etl.ipynb`: This is a jupyter notebook file which has the same content as `etl.py`
- `test.ipynb`: This file is a jupyter notebook file to run queries to confirm the creation of tables. 

## Running the project
To run this project, please make sure the connection strings in `create_tables.py` and `etl.py` contain the credentials for your 
postgres server. 
- Next you you run the following command to create the database and tables `python create_tables.py`
- Furthermore, to develop ETL processes for each table, run `python etl.py`


## Example Queries and Results
### Retrieve 10 song played by users
Run the following queries from psql terminal
`SELECT * FROM songplays LIMIT 2;`


` songplay_id |  start_time   | user_id | level | song_id | artist_id | session_id | location user_agent`                                     
`-------------+---------------+---------+-------+---------+-----------+------------+-------------------------+-----------------------------------------------------------------------------------`
`0 | 1542326457796 | 44      | paid  |         |           |        637 | Waterloo-Cedar Falls, IA | Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:31.0) Gecko/20100101 Firefox/31.0`
`1 | 1542326688796 | 44      | paid  |         |           |        637 | Waterloo-Cedar Falls, IA | Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:31.0) Gecko/20100101 Firefox/31.0`


### Retrieve 5 users of the app
`SELECT * FROM users LIMIT 5;`


` user_id | first_name | last_name | gender | level `
`---------+------------+-----------+--------+-------`
`      61 | Samuel     | Gonzalez  | M      | free  `
`      88 | Mohammad   | Rodriguez | M      | paid  `
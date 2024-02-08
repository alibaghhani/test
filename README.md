# PostgreSQL Database Interaction

This Python script provides a simple interface to interact with a PostgreSQL database. It allows you to perform basic CRUD (Create, Read, Update, Delete) operations on a table named 'simple' in your PostgreSQL database.

## Prerequisites

Before using this script, ensure you have the following:

- Python installed on your system.
- psycopg2 library installed. You can install it using pip:
- pip install psycopg2


## Setup

1. Clone or download this repository to your local machine.

2. Modify the connection parameters in the `main()` function of `database.py` according to your PostgreSQL database configuration:
 - `database`: Name of your database.
 - `user`: Username for the database.
 - `password`: Password for the database.
 - `host`: Hostname of the PostgreSQL server.
 - `port`: Port number on which the PostgreSQL server is running.

## Usage

1. Run the `database.py` script:

2. You will be presented with a menu to choose your operation:
- Insert data
- Select data
- Update data
- Delete data
- Filter data
- Exit

3. Follow the prompts to perform your desired operation.

## Notes

- This script logs all database interactions to a file named `database.log` in the same directory. You can adjust the logging configuration in the `__init__()` method of the `Database` class in `database.py`.
- Ensure you have proper permissions and configurations set up in your PostgreSQL database for the user specified in the script.

Feel free to customize and extend this script as per your requirements!

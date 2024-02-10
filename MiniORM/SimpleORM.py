import logging
import psycopg2
from psycopg2 import OperationalError


class Database:
    """A class to interact with a PostgreSQL database."""

    def __init__(self, database, user, password, host, port):
        """Initialize Database class with connection parameters."""
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.log_file = 'database.log'
        self.log_handler = logging.FileHandler(self.log_file)
        self.log_handler.setFormatter(self.log_formatter)
        self.logger.addHandler(self.log_handler)

    def connect(self):
        """Establish a connection to the database."""
        try:
            self.connection = psycopg2.connect(
                database=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.logger.info("Database connection established successfully")
        except OperationalError as e:
            self.logger.error(f"Error: {e}")

    def disconnect(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.logger.info("Database connection closed")

    def execute_query(self, query, params=None):
        """
        Execute a SQL query.

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters for the query. Defaults to None.

        Returns:
            int: Number of affected rows.
        """
        if not self.connection:
            self.logger.warning("No database connection")
            return -1

        try:
            cur = self.connection.cursor()
            cur.execute(query, params)
            self.connection.commit()
            cur.close()
            self.logger.info("Query executed successfully")
            return cur.rowcount
        except (psycopg2.Error, Exception) as e:
            self.connection.rollback()
            self.logger.error(f"Error executing query: {e}")
            return -1

    def create_table_query(self):
        """Create the 'simple' table in the database."""
        query = """
            CREATE TABLE IF NOT EXISTS simple (
                admission SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                age INTEGER NOT NULL,
                course VARCHAR(255) NOT NULL,
                department VARCHAR(255) NOT NULL
            )
        """
        self.execute_query(query)

    def insert_data(self, name, age, course, department):
        """
        Insert data into the 'simple' table.

        Args:
            name (str): Name of the person.
            age (int): Age of the person.
            course (str): Course of the person.
            department (str): Department of the person.

        Returns:
            int: Number of affected rows.
        """
        query = "INSERT INTO simple (name, age, course, department) VALUES (%s, %s, %s, %s)"
        params = (name, age, course, department)
        return self.execute_query(query, params)

    def select_data(self):
        """Select and print data from the 'simple' table."""
        query = "SELECT admission, name, age, course, department FROM simple"
        try:
            cur = self.connection.cursor()
            cur.execute(query)
            rows = cur.fetchall() # noqa
            cur.close()
            if rows:
                for row in rows:
                    print("ADMISSION =", row[0])
                    print("NAME =", row[1])
                    print("AGE =", row[2])
                    print("COURSE =", row[3])
                    print("DEPARTMENT =", row[4], "\n")
            else:
                print("No data found")
        except psycopg2.Error as e:
            self.logger.error(f"Error selecting data: {e}")

    def update_data(self, admission_number, new_age):
        """
        Update the age of a record in the 'simple' table.

        Args:
            admission_number (int): Admission number of the record to update.
            new_age (int): New age value.

        Returns:
            int: Number of affected rows.
        """
        query = "UPDATE simple SET age = %s WHERE admission = %s"
        params = (new_age, admission_number)
        return self.execute_query(query, params)

    def delete_data(self, admission_number):
        """
        Delete a record from the 'simple' table.

        Args:
            admission_number (int): Admission number of the record to delete.

        Returns:
            int: Number of affected rows.
        """
        query = "DELETE FROM simple WHERE admission = %s"
        params = (admission_number,)
        return self.execute_query(query, params)

    def filter_data(self, condition, params=None):
        """
        Select and print filtered data from the 'simple' table.

        Args:
            condition (str): The WHERE condition for filtering.
            params (tuple, optional): Parameters for the condition. Defaults to None.

        Returns:
            None
        """
        query = f"SELECT admission, name, age, course, department FROM simple WHERE {condition}"
        try:
            cur = self.connection.cursor()
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            rows = cur.fetchall() # noqa
            cur.close()
            if rows:
                for row in rows:
                    print("ADMISSION =", row[0])
                    print("NAME =", row[1])
                    print("AGE =", row[2])
                    print("COURSE =", row[3])
                    print("DEPARTMENT =", row[4], "\n")
            else:
                print("No data found")
        except psycopg2.Error as e:
            self.logger.error(f"Error filtering data: {e}")


def main():
    logging.basicConfig(level=logging.DEBUG)
    db = Database("postgres", "pedram", "pedram@karimi", "127.0.0.1", "5432")
    db.connect()
    db.create_table_query()

    while True:
        print("\nOptions:")
        print("1. Insert data")
        print("2. Select data")
        print("3. Update data")
        print("4. Delete data")
        print("5. Filter data")
        print("6. Exit\n")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter name: ")
            age = int(input("Enter age: "))
            course = input("Enter course: ")
            department = input("Enter department:")
            db.insert_data(name, age, course, department)
        elif choice == '2':
            db.select_data()
        elif choice == '3':
            admission_number = int(input("\nEnter admission number to update: "))
            new_age = int(input("\nEnter new age: "))
            db.update_data(admission_number, new_age)
        elif choice == '4':
            admission_number = int(input("\nEnter admission number to delete: "))
            db.delete_data(admission_number)
        elif choice == '5':
            condition = input("\nEnter WHERE condition: ")
            db.filter_data(condition)
        elif choice == '6':
            break
        else:
            print("Invalid choice\n")

    db.disconnect()


if __name__ == "__main__":
    main()

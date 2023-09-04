from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Access the Neo4j host, username, and password
neo4j_host = os.environ.get("NEO4J_HOST")
neo4j_username = os.environ.get("NEO4J_USERNAME")
neo4j_password = os.environ.get("NEO4J_PASSWORD")


class Neo4jDriverSingleton:
    """
    Singleton class for interacting with Neo4j database

    """
    _instance = None

    def __new__(cls, uri, user, password):
        if cls._instance is None:
            cls._instance = super(Neo4jDriverSingleton, cls).__new__(cls)
            cls._instance._driver = GraphDatabase.driver(
                uri, auth=(user, password))
        return cls._instance

    def close(self):
        self._driver.close()

    def session(self):
        """
        Return a new session object for interacting with Neo4j.

        :return: Neo4j session
        """
        return self._driver.session()


def insert_data(filename):
    """
    Function to insert data into Neo4j database

    :param name: name of the person
    :param age: age of the person
    :return: None
    """
    try:

        with open(filename, 'r') as fp:
            data = fp.read()

        # Cypher query to insert data into Neo4j
        insert_query = f"CREATE {data}"

        # Create a session explicitly
        with neo4j_driver.session() as session:
            # Execute the insert query
            session.run(insert_query)

        print("Data inserted successfully")

    except Exception as e:
        print(f"An error occurred while inserting data: {str(e)}")


def fetch_data():
    """
    Generator function to fetch data from Neo4j database

    Yields: records from Neo4j database
    """
    try:
        # Cypher query to fetch data from Neo4j
        fetch_query = "MATCH (n) RETURN n"

        # Create a session explicitly
        with neo4j_driver.session() as session:
            # Execute the fetch query
            result = session.run(fetch_query)

            # Iterate through the result and yield records one by one
            for record in result:
                # Assuming 'n' is the property you want to access
                yield record["n"]

    except Exception as e:
        print(f"An error occurred while fetching data: {str(e)}")


def delete_data():
    """
    Function to delete data from Neo4j database

    :param name: name of the person to be deleted
    :return: None
    """
    try:
        # Cypher query to delete data from Neo4j based on name
        delete_query = "MATCH (n) DETACH DELETE n"

        # Create a session explicitly
        with neo4j_driver.session() as session:
            # Execute the delete query
            session.run(delete_query)

        print(f"Data deleted successfully")

    except Exception as e:
        print(f"An error occurred while deleting data: {str(e)}")


if __name__ == "__main__":
    # Define your Neo4j database credentials
    neo4j_uri = neo4j_host
    neo4j_user = neo4j_username
    neo4j_password = neo4j_password

    # Create a Neo4j driver instance using the Singleton
    neo4j_driver = Neo4jDriverSingleton(neo4j_uri, neo4j_user, neo4j_password)

    try:
        # inserting data into Neo4j:
        # insert_data('data.txt')

        # Fetch data from Neo4j database using the generator

        for record in fetch_data():
            print(record['name'])

        # delete all data from Neo4j db:
        # delete_data()

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # The generator will automatically close the result when exhausted
        neo4j_driver.close()

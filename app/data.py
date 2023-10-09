from os import getenv
from typing import Dict, Iterable, Iterator
# from random import randrange

from certifi import where
from dotenv import load_dotenv
from MonsterLab import Monster
from pandas import DataFrame
from pymongo import MongoClient


class Database:
    """
    The Database class is an interface between a Pymongo database
    hosted on Atlas https://cloud.mongodb.com/ using MongoClient.

    The interface supports CRUD, and has business logic functions as well.
    There are also functions to seed the database, reset it, wrap the data
    in a dataframe, and create a html table from a dataframe.

    Class Attributes:
    ---------
    None

    Instance Attributes: (defined in __init__() )
    ---------
    self.client : MongoClient
        A database driver for a MongoDB. The connection.
    self.db : PyMongo Database (https://pymongo.readthedocs.io/en/stable/api/pymongo/database.html#pymongo.
    database.Database)
        A PyMongo Database object. The specific database.
    self.Collection : PyMongo Collection object (https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.
    html#pymongo.collection.Collection)
        A PyMongo Collection object. The specific collection.

    Init and CRUD Methods:
    ---------
    __init__(self) -> None:
        Initializes a PyMongo Connection, with instance objects: client, db, Collection
    create_one(self, record: Dict = None) -> bool:
        CRUD method: creates a single Monster in the database.
    read_one(self, query: Dict = None) -> Dict:
        CRUD method: reads a single record matching the query.
    update_one(self, query: Dict, update: Dict) -> bool:
        CRUD method: updates a record in the database using a query and an update dictionary.
    delete_one(self, query: Dict) -> bool:
        CRUD method: deletes a single record in the database using a query.
    create_many(self, records: Iterable[Dict]) -> bool:
        CRUD method: creates many record in the database using an iterable
        containing dictionary records.
    read_many(self, query: Dict) -> Iterator[Dict]:
        CRUD method: reads many records from the database that match query.
    update_many(self, query: Dict, update: Dict) -> bool:
        CRUD method: updates many records that match query with update dictionary.
    delete_many(self, query: Dict) -> bool:
        CRUD method: deletes many records that match query.

    Business logic methods:
    ---------
    seed(self, amount: int):
        Creates the input amount of Monsters in the database.
    reset(self):
        Resets the database to be empty.
    count(self) -> int:
        Returns a count of the total objects in the database's current collection.
    dataframe(self) -> DataFrame:
        Returns a Pandas dataframe with all objects in the database's current collection.
    html_table(self) -> str:
        Returns a string containing a html table of all the Monsters
        in the database's current collection.
    """

    def __init__(self) -> None:
        """
        The init function creates a connection to the Atlas hosted database
        using an environment file string. And also sets class variables for
        the database 'db' and the Monster collection 'collection'

        :return: Database, an instance of the Database interface class
        with instance attributes.
        """

        # Load environmental variables
        load_dotenv()

        # Create a connection to the MongoDB server
        self.client = MongoClient(getenv("DB_URL"), tlsCAFile=where())

        # Select the database
        self.db = self.client['Database']

        # Select the collection
        self.collection = self.db['Monsters']

    def create_one(self, record: Dict = None) -> bool:
        """
        CRUD method: creates a single Monster in the database.

        If no input Monster record is given, it creates a random Monster.
        It uses the pymongo insert_one method: https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#
        pymongo.collection.Collection.insert_one
        It returns a bool as type pymongo.results.InsertOneResult

        :param record: Dict, the attributes of the Monster to create.
        :return: bool, representing if the Monster was created.
        """
        if record is None:
            record = Monster().to_dict()
        return self.collection.insert_one(record).acknowledged

    def read_one(self, query: Dict = None) -> Dict:
        """
        CRUD method: reads a single record matching the query.

        If no query is given, then it returns the first record.
        In the MongoDB context, passing None as the query to find_one will
        return the first document in the collection without any filter,
        excluding the _id field.

        :param query: Dict, the attributes to find a single Monster.
        :return: Dict, the attributes of the found Monster.
        """
        # if query is None:
        #     pipeline = [
        #         {'$sample': {'size': 1}}
        #     ]
        #     record = list(self.collection.aggregate(pipeline))
        return self.collection.find_one(query, {"_id": False})

    def update_one(self, query: Dict, update: Dict) -> bool:
        """
        CRUD method: updates a record in the database using a query and an update dictionary.

        and updates the first matching record to the query with the new info.
        The $set operator replaces the value of the field or creates it if is does
        not exist.
        Returns a pymongo.results.UpdateResult which has properties: acknowledged,
        matched_count (num of docs matching), modified_count (num of docs modified),
        raw_result(raw doc returned from server), upserted_id (id of upserted doc)

        :param query: Dict, the attributes to match to find a single Monster to update.
        :param update: Dict, the attributes to update.
        :return: bool, representing if the Monster was updated.
        """
        return self.collection.update_one(query, {"$set": update}).acknowledged

    def delete_one(self, query: Dict) -> bool:
        """
        CRUD method: deletes a single record in the database using a query.

        :param query: Dict, the Monster attributes to find and delete a single Monster.
        :return: bool, representing if the Monster was deleted.
        """
        return self.collection.delete_one(query).acknowledged

    def create_many(self, records: Iterable[Dict]) -> bool:
        """
        CRUD method: creates many record in the database using an iterable
        containing dictionary records.

        :param records: Iterable[Dict], Dicts of Monsters to create.
        :return: bool, representing if the Monsters were created.
        """
        return self.collection.insert_many(records).acknowledged

    def read_many(self, query: Dict) -> Iterator[Dict]:
        """
        CRUD method: reads many records from the database that match query.

        :param query: Dict, Monster attributes to find matching Monsters.
        :return: bool, representing if Monsters are found.
        """
        return self.collection.find(query, {"_id": False})

    def update_many(self, query: Dict, update: Dict) -> bool:
        """
        CRUD method: updates many records that match query with update dictionary.

        :param query: Dict, Monster attributes to find Monsters to update.
        :param update: Dict, the attribute changes to be made to matching Monsters.
        :return: bool, representing if the Monsters were updated.
        """
        return self.collection.update_many(query, {"$set": update}).acknowledged

    def delete_many(self, query: Dict) -> bool:
        """
        CRUD method: deletes many records that match query.

        :param query: Dict, Monster attributes that are used to delete Monsters
        from the database.
        :return: bool, representing if the objects were deleted successfully.
        """
        return self.collection.delete_many(query).acknowledged

    def seed(self, amount: int):
        """
        Creates the input amount of Monsters in the database.

        :param amount: int, the desired number of Monsters to create in the database.
        :return: bool, representing if the objects were created successfully.
        """
        records = [Monster().to_dict() for _ in range(amount)]
        return self.create_many(records)

    def reset(self):
        """
        Resets the database to be empty.

        :return: bool, representing if the objects were deleted successfully.
        """
        records = {}
        return self.delete_many(records)

    def count(self) -> int:
        """
        Returns a count of the total objects in the database's current collection.

        :return: int, count of Monsters.
        """
        query = {}
        count = self.collection.count_documents(query)  # {} means no filter, so it counts all documents
        print(f'There are {count} documents in the collection.')
        return count

    def dataframe(self) -> DataFrame:
        """
        Returns a Pandas dataframe with all objects in the database's current collection.

        :return: Pandas DataFrame object, of Monsters.
        """
        query = {}
        df = DataFrame(list(self.read_many(query)))
        return df

    def html_table(self) -> str:
        """
        Returns a string containing a html table of all the Monsters
        in the database's current collection.

        :return: str, html formatted in a table.
        """
        df = self.dataframe()
        html_table = df.to_html(border=1, classes='dataframe', index=True)
        return html_table


if __name__ == '__main__':
    '''
    This code is run when data.py file is the main program.
    If imported into another file, this block of code will not run.
    '''
    print('Running data.py, the Database interface, as main...')

    db = Database()

    print(f'The client: {db.client}')

    databases = db.client.list_database_names()
    print(f'The databases: {databases}')

    # use list_collection_names method to get a list of all collection names
    collections = db.client.list_collection_names()
    # print the collections
    for collection in collections:
        print(f'Collection: {collection}')

import sys
import pytest
from pymongo import MongoClient
from app.data import Database
from os import getenv
from dotenv import load_dotenv
from certifi import where
from MonsterLab import Monster

print(sys.path)


# Setup a fixture to provide a test database connection
@pytest.fixture
def test_db():
    load_dotenv()

    # client = MongoClient('localhost', 27017)
    client = MongoClient(getenv("DB_URL"), tlsCAFile=where())

    # Select the database
    db = client['Database']

    # Select the collection
    # collection = db['Monsters']

    yield db


# Example test for the create_one function
# def test_create_one(test_db):
#     collection = test_db['Monsters']
#     monster = {"name": "Test Monster", "type": "Dragon"}
#
#     # Call the function to test
#     acknowledged = data.create_one(monster)
#
#     # Check if the record was created
#     assert acknowledged == True
#
#     # Additional check to confirm the record exists in the database
#     created_monster = collection.find_one({"name": "Test Monster"})
#     assert created_monster is not None
#     assert created_monster["name"] == "Test Monster"
#     assert created_monster["type"] == "Dragon"


def test_create_one_example():
    # Create an instance of the Database class
    database = Database()

    # Define a record to create
    record = {'Name': 'Example Monster', 'Type': 'Dragon'}

    # Call the create_one method
    result = database.create_one(record)

    # Assert something about the result (e.g., that it's True, or check the database to make sure the record was
    # inserted)
    assert result


def test_create_one_random():
    # Create an instance of the Database class
    database = Database()

    # Call the create_one method
    result = database.create_one()

    # Assert something about the result (e.g., that it's True, or check the database to make sure the record was
    # inserted)
    assert result


def test_read_one_demonic():
    # Create an instance of the Database class
    database = Database()

    # Query to find a record with "Type": "Demonic"
    query = {"Type": "Demonic"}

    # Use the read_one method to find the first such record
    record = database.read_one(query)
    print(record)

    # Assert that the record is not None and has the expected "Type" field
    assert record is not None
    assert record['Type'] == 'Demonic'


def test_read_one_random():
    # Create an instance of the Database class
    database = Database()

    # Call the create_one method
    result = database.read_one()
    print(result)

    # Assert something about the result (e.g., that it's True, or check the database to make sure the record was
    # inserted)
    assert result is not None


# Updates a monster of name: 'Example Monster' to new info
def test_update_one_example_monster():
    # Create an instance of the Database class
    database = Database()

    # Update query
    query = {'Name': 'Example Monster', 'Type': 'Dragon'}

    # Update info
    update = {
        'Name': 'Example Monster Updated',
        'Type': 'Copper Drake',
        'Level': 42,
        'Rarity': 'Rank 2',
        'Damage': '42d4+1',
        'Health': 89.72,
        'Energy': 130.03,
        'Sanity': 83.58
    }

    database.update_one(query, update)

    # Assert that the correct record has been updated


def test_delete_one_devilkin():
    # Create an instance of the Database class
    database = Database()

    query = {'Type': 'Devilkin'}

    database.delete_one(query)

    # Assert deletion has happened


def test_create_many_10():
    # Create an instance of the Database class
    database = Database()

    # Create 10 monsters
    monsters = [Monster().to_dict() for _ in range(10)]
    print(monsters)

    # for monster in monsters:
    #     database.create_one(monster)

    database.create_many(monsters)

    # Assert some things:
    assert len(monsters) == 10
    # Assert that 10 new monsters have been added to the database (the overall count has increased 10?)


def test_read_many_random():
    # Create an instance of the Database class
    database = Database()

    # Call the create_one method
    query = {'Type': 'Dragon'}
    result = database.read_many(query)
    print(result)

    # Assert something about the result (e.g., that it's True, or check the database to make sure the record was
    # inserted)
    assert result is not None
    # assert result.length > 1


def test_update_many_demonic_monsters():
    # Create an instance of the Database class
    database = Database()

    # Update query
    query = {'Type': 'Demonic'}

    # Update info
    update = {
        'Name': 'Demonic Monster Health 150',
        'Health': 150.00
    }

    database.update_one(query, update)

    # Assert that the correct records have been updated
    first_monster = database.read_one({'Name': 'Demonic Monster Health 150'})
    print(first_monster)
    health = first_monster['Health']
    print(health)
    assert health == 150


def test_delete_many_undead():
    # Create an instance of the Database class
    database = Database()

    query = {'Type': 'Undead'}

    database.delete_many(query)

    # Assert deletion has happened
    assert database.read_one(query) is None


def test_seed_100():
    # Create an instance of the Database class
    database = Database()

    # Create 100 monsters
    # monsters = [Monster().to_dict() for _ in range(100)]
    # print(monsters)

    # for monster in monsters:
    #     database.create_one(monster)

    # database.create_many(monsters)
    database.seed(100)

    # Assert some things:
    # assert len(monsters) == 100
    # Assert that 10 new monsters have been added to the database (the overall count has increased 10?)

def test_seed_1000():
    # Create an instance of the Database class
    database = Database()

    # Create 1000 monsters
    # monsters = [Monster().to_dict() for _ in range(100)]
    # print(monsters)

    # for monster in monsters:
    #     database.create_one(monster)

    # database.create_many(monsters)
    database.seed(1000)

    # Assert some things:
    # assert len(monsters) == 100
    # Assert that 10 new monsters have been added to the database (the overall count has increased 10?)


def test_reset_delete_all():
    # Create an instance of the Database class
    database = Database()

    query = {}

    database.reset()

    # Assert deletion has happened
    assert database.read_one(query) is None


def test_count():
    database = Database()

    print(database.count())


def test_dataframe():
    database = Database()

    df = database.dataframe()
    # print(df[0])
    print('First item in the dataframe object is: ', df.head(1))

    # Assert dataframe object contains all objects in collection
    assert df.shape[0] == database.count()


def test_dataframe_export_csv():
    database = Database()

    df = database.dataframe()
    # print(df[0])
    print('First item in the dataframe object is: ', df.head(1))

    # Save local csv file of Monsters
    df.to_csv('monsters.csv', index=False)

    # Assert dataframe object contains all objects in collection
    assert df.shape[0] == database.count()


def test_html_table():
    database = Database()

    table_string = database.html_table()

    print(table_string[1:6])

    print(table_string)

    assert table_string[1:6] == 'table'

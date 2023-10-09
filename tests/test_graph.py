import sys
import pytest
from pymongo import MongoClient
from app.data import Database
from os import getenv
from dotenv import load_dotenv
from certifi import where
from MonsterLab import Monster
from app.graph import chart
from pandas import DataFrame
import altair as alt

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

def test_graph_is_generated():
    # Sample data for testing
    data = {
        'A': [1, 2, 3],
        'B': [4, 5, 6],
        'C': ['p', 'q', 'r']
    }
    df = DataFrame(data)

    # Generate the chart
    generated_chart = chart(df, 'A', 'B', 'C')

    # Check if the generated chart is an instance of altair.Chart
    assert isinstance(generated_chart, alt.Chart)

    # Check if the chart has the expected title
    assert generated_chart.title == "B by A for C"

def test_chart_serialization():
    # Sample data for testing
    data = {
        'A': [1, 2, 3],
        'B': [4, 5, 6],
        'C': ['p', 'q', 'r']
    }
    df = DataFrame(data)

    # Generate the chart
    original_chart = chart(df, 'A', 'B', 'C')

    # Serialize the chart to JSON
    serialized_chart = original_chart.to_json()

    # Deserialize the JSON back into a chart
    deserialized_chart = alt.Chart.from_json(serialized_chart)

    print(original_chart.encoding)
    print('#################################')
    print(deserialized_chart.encoding)

    # Compare properties of the original and deserialized charts
    # assert original_chart.encoding == deserialized_chart.encoding

    # Compare the serialized JSON strings
    # This is more stringent as it checks for exact match
    # assert original_chart.to_json() == deserialized_chart.to_json()

    # Compare essential properties of the original and deserialized charts
    # assert original_chart.encoding.x.shorthand == deserialized_chart.encoding.x.field
    # assert original_chart.encoding.y.shorthand == deserialized_chart.encoding.y.field
    # assert original_chart.encoding.color.shorthand == deserialized_chart.encoding.color.field


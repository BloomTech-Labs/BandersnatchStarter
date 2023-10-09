import sys
import pytest
from app.data import Database
from app.machine import Machine
from joblib import load, dump
import os
from flask import Flask, render_template, request
from Fortuna import random_int, random_float
from unittest.mock import Mock, patch
import numpy as np
from pandas import DataFrame


print(sys.path)

APP = Flask(__name__)


@pytest.fixture
def test_db():
    db = Database()
    yield db

''' 
* Does the __init__ function properly initialize the machine learning 
model and store it as an attribute?
* Does the class properly handle and store the target and feature data 
when initializing the model?
'''
def test_init(test_db):
    df = test_db.dataframe()

    # Make a Machine object with the dataframe
    options = ["Level", "Health", "Energy", "Sanity", "Rarity"]
    machine = Machine(df[options])

    # Test Machine object outputs match expected
    print("-----------------")
    print("test_init checks: All the machine attributes:")
    print(f"Machine name: {machine.name}")
    print(f"Timestamp: {machine.timestamp}")
    print(f"Target: {machine.target[:3]}")
    print(f"Features: {machine.features[:3]}")
    print(f"Model: {machine.model}")
    print(f"Info(): {machine.info()}")
    print("-----------------")


'''
* Does the __call__ function take in a DataFrame of feature data and 
return a prediction and the probability of the prediction?
'''
def test_call(test_db):
    options = ["Level", "Health", "Energy", "Sanity", "Rarity"]
    filepath = os.path.join("..", "app", "model.joblib")
    print(options, filepath)
    if not os.path.exists(filepath):
        print("if not")
        df = test_db.dataframe()
        machine = Machine(df[options])
        machine.save(filepath)
    else:
        print('else')
        machine = Machine.open(filepath)
        print(machine)
    stats = [round(random_float(1, 250), 2) for _ in range(3)]
    level = request.values.get("level", type=int) or random_int(1, 20)
    health = request.values.get("health", type=float) or stats.pop()
    energy = request.values.get("energy", type=float) or stats.pop()
    sanity = request.values.get("sanity", type=float) or stats.pop()
    print(stats, level, health, energy, sanity)
    print(f"Stats: {stats}")
    prediction, confidence = machine(DataFrame(
        [dict(zip(options, (level, health, energy, sanity)))]
    ))
    print(f"Prediction {prediction}. Confidence {confidence}")
    return 'Done'

def test_call2(test_db):
    df = test_db.dataframe()
    options = ["Level", "Health", "Energy", "Sanity", "Rarity"]
    machine = Machine(df[options])
    level = random_int(1, 20)
    stats = [round(random_float(1, 250), 2) for _ in range(3)]
    health = stats.pop()
    energy = stats.pop()
    sanity = stats.pop()
    print(level, health, energy, sanity)
    prediction, confidence = machine(DataFrame([dict(zip(options, (level, health, energy, sanity)))]))
    print(prediction, confidence)

# Test function using pytest
def test_machine_call():
    # Mock model and its predict method
    mock_model = Mock()
    mock_model.predict.return_value = [np.array([1.0])]

    # Create an instance of Machine with the mock model
    machine = Machine(mock_model)

    # Test input
    feature_basis = np.array([0.5, 0.4, 0.1])

    # Create a test client and request context
    with APP.test_request_context('/?level=1'):
        # Call the instance (tests the __call__ method)
        prediction = machine(feature_basis)

        # Assert that model.predict was called with the correct argument
        mock_model.predict.assert_called_once_with([feature_basis])

        # Assert the output is as expected
        assert np.array_equal(prediction, np.array([1.0]))


def test_model():
    with APP.test_client() as client:
        # Send a GET request to the route
        response = client.get('/model?level=1')

        # Check the response data/status code
        assert response.status_code == 200
        assert b'Expected response data' in response.data


'''
Does `save()` properly save the machine learning model to the specified 
filepath using joblib?
'''
def test_save_model(test_db):
    machine = test_init(test_db)
    model_path = os.path.abspath(os.path.join(cwd, '..', 'app', 'model.joblib'))
    machine.save(model_path)


'''
Does `open()` properly load a saved machine learning model from the 
specified filepath using joblib?
'''
def test_open_model(test_db):
    # Get the current working directory
    cwd = os.getcwd()

    # Get the absolute path to 'model.joblib'
    model_path = os.path.abspath(os.path.join(cwd, '..', 'app', 'model.joblib'))

    model = load(model_path)
    print(model)

    df = test_db.dataframe()
    machine = Machine(df)
    print(machine.model)

    assert str(model) == 'RandomForestClassifier(random_state=42)'


'''
Does `info()` return a string with the name of the base model and 
the timestamp of when it was initialized? like this:
Base Model: Random Forest Classifier
Timestamp: 2023-09-08 9:29:50 PM
'''
def test_info_about_model(test_db):
    # Are you connected ot the test_db fixture?
    df = test_db.dataframe()
    print(df.head(3))

    # Make a Machine object with the dataframe
    machine = Machine(df=df)
    print(machine.info())

    assert machine.name == 'Random Forest Classifier'


def test_fortuna(test_db):
    from Fortuna import random_int, random_float
    stats = [round(random_float(1, 250), 2) for _ in range(3)]
    print(stats)


# def test_requests(test_db):
#     app = create_app()
#     with app.test_request_context('/example?key=value'):
#         options = ["Level", "Health", "Energy", "Sanity", "Rarity"]
#         stats = [round(random_float(1, 250), 2) for _ in range(3)]
#         level = request.values.get("level", type=int) or random_int(1, 20)
#         health = request.values.get("health", type=float) or stats.pop()
#         energy = request.values.get("energy", type=float) or stats.pop()
#         sanity = request.values.get("sanity", type=float) or stats.pop()


@pytest.fixture
def client():
    APP.config['TESTING'] = True
    with APP.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    print(response.data)
    #assert response.data == b'Hello, Flask!'

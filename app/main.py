from base64 import b64decode
import os

from Fortuna import random_int, random_float
from MonsterLab import Monster
from flask import Flask, render_template, request, redirect, url_for
from pandas import DataFrame

from app.data import Database
from app.graph import chart
from app.machine import Machine, PROJECT_ROOT

import logging


logging.basicConfig(filename='application.log', level=logging.DEBUG)

SPRINT = 3
APP = Flask(__name__)


@APP.route("/")
def home():
    return render_template(
        "home.html",
        sprint=f"Sprint {SPRINT}",
        monster=Monster().to_dict(),
        password=b64decode(b"VGFuZ2VyaW5lIERyZWFt"),
    )


@APP.route("/data")
def data():
    if SPRINT < 1:
        return render_template("data.html")
    db = Database()
    return render_template(
        "data.html",
        count=db.count(),
        table=db.html_table(),
    )


@APP.route("/view", methods=["GET", "POST"])
def view():
    if SPRINT < 2:
        return render_template("view.html")

    db = Database()

    options = ["Level", "Health", "Energy", "Sanity", "Rarity"]

    x_axis = request.values.get("x_axis") or options[1]
    y_axis = request.values.get("y_axis") or options[2]
    target = request.values.get("target") or options[4]

    graph = chart(
        df=db.dataframe(),
        x=x_axis,
        y=y_axis,
        target=target,
    ).to_json()

    return render_template(
        "view.html",
        options=options,
        x_axis=x_axis,
        y_axis=y_axis,
        target=target,
        count=db.count(),
        graph=graph,
    )


@APP.route("/model", methods=["GET", "POST"])
def model():
    logging.debug("Entered model route")

    if SPRINT < 3:
        return render_template("model.html",
                               level = 4)

    else:
        # Setup:
        # Create a database instance and dataframe instance.
        db = Database()
        df = db.dataframe()


        # Create a Machine instance.
        # (In __init__(), Try to load an existing model. If no model exists, train one).
        # Use __init__() with open(). OR train a model and save it with save(). Fill in machine attributes using
        # the model (loaded or created) and info().
        machine = Machine(df)


        # Assign the variables to load the page:
        info = machine.info()
        level = request.values.get("level", type=int) or random_int(1, 20)
        stats = [round(random_float(1, 250), 2) for _ in range(3)]
        health = request.values.get("health", type=float) or stats.pop()
        energy = request.values.get("energy", type=float) or stats.pop()
        sanity = request.values.get("sanity", type=float) or stats.pop()


        # Make a Prediction.
        # If no values are present in the form, give random numbers. And immediately use those random
        # numbers to predict Rarity with a confidence number using the existing model (either loaded or trained).
        # Use __call__() to make a prediction

        options = ["Level", "Health", "Energy", "Sanity", "Rarity"]
        prediction, confidence = machine(DataFrame([dict(zip(options, (level, health, energy, sanity)))]))
        print(f"Labels are: {machine.labels}, type: {type(machine.labels)}")
        string_prediction = machine.labels[prediction]
        print(f"String prediction is: {string_prediction}")
        print(f"Prediction {prediction}. Confidence {confidence}")


        # Make a new Prediction.
        # Option A - yes retrain)
        # If the user changes those numbers and clicks the button ‘Retrain’, then create a new model
        # (with the full database), save it, make a prediction (with the input numbers) and return that prediction.
        # Delete the model.
        # Then create a new Machine instance
        retrain = request.form.get('retrain')
        print(f"Retrain: {retrain}")

        if retrain == 'True':
            # Checkbox was checked
            print("Retrain is checked")
            filepath = os.path.join(PROJECT_ROOT, 'app', 'model.joblib')

            # Check if the model file exists, then delete it
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"Model file at {filepath} has been deleted")

                machine.retrain(df)

                options = ["Level", "Health", "Energy", "Sanity", "Rarity"]
                prediction, confidence = machine(DataFrame([dict(zip(options, (level, health, energy, sanity)))]))
                print(f"Labels are: {machine.labels}, type: {type(machine.labels)}")
                string_prediction = machine.labels[prediction]
                print(f"String prediction is: {string_prediction}")
                print(f"Prediction {prediction}. Confidence {confidence}")

            else:
                print(f"No such model file at {filepath}")

        else:
            # Checkbox was not checked
            print("Retrain is not checked")
            # Option B - no retrain)
            # If the user changes those numbers and clicks ‘predict rarity’ (without ‘Retrain’
            # clicked) then use the existing loaded model, and new numbers, to make a prediction and return that
            # prediction.
            # The prediction/confidence will change automatically as the page is reloaded when the button is clicked.

        return render_template(
            "model.html",
            info=info,
            level=level,
            health=health,
            energy=energy,
            sanity=sanity,
            prediction=string_prediction,
            confidence=f"{confidence:.2%}",
        )

if __name__ == '__main__':
    APP.run(debug=True)

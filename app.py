import os
import logging
from pymongo import MongoClient
from flask import Flask, request
from jsonschema import validate, ValidationError
from dotenv import load_dotenv
import validation_schemas

load_dotenv()

app = Flask(__name__)
app.logger.setLevel("INFO")
app.logger.info("Hello!")

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
client = MongoClient(os.getenv("DATABASE_URL"))
db = client.starbase0

@app.route("/", methods = ["POST"])
def hello():
    try:
        app.logger.info("hello was called")

        data = request.json
        app.logger.info("request: %s", data)
        validate(data, validation_schemas.request)

        name = data["name"]

        person = db.people.find_one({"name": name})
        app.logger.info("database item found: %s", person)

        response = {"message": "Hello " + person["name"] + "!"}
        validate(response, validation_schemas.response)

        return response

    except Exception as inst:
        app.logger.error(inst)
    
    return {"message": "Did not find person."}
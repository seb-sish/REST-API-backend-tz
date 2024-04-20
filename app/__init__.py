from flask import Flask, jsonify, request, abort
from flask_restful import Api, Resource
from config import Config
app = Flask(__name__)
api = Api(app)

app.config.from_object(Config)
from app import routes
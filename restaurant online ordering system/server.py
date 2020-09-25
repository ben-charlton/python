from flask import Flask
from init import bootstrap_system
from src.ingredient import Ingredient

app = Flask(__name__)
app.secret_key = 'very-secret-123'  # Used to add entropy

system = bootstrap_system()

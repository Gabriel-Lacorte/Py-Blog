# app/__init__.py
from flask import Flask
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

from app import views


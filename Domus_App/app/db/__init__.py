from models import db_meta
from app import app
from flask_sqlalchemy import SQLAlchemy

# biz logic taken from controller
class Database(metaclass=db_meta):
    def __init__(self) -> None:
        db = SQLAlchemy(app)
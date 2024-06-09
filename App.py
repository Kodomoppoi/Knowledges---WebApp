from sqlalchemy import crate_engine, String, Interger, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///minhabase.sqlite3'
db = SQLAlchemy(app)
app.app_context().push()

#criação da db com sql alchemy

class Users(db.model):
    __tablename__ = "users"

    #a db de cada usuario consistirá em  integer {{id}} único, string {{username}}, string {{topic_1}}, string {{topic_2}},integer {{complexity}}
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique = True, nullable = False)
    topic_1 = db.Coluumn(db.String, nullable = False)
    topic_2 = db.Column(db.String, nullable = False)
    complexity = db.Column(db.integer)

    def __init__(self, id, username, topic_1, topic_2, complexity):
        self.id = id
        self.username = username
        self.topic_1 = topic_1
        self.topic_2 = topic_2
        self.complexity = complexity




if __name__ == "__main__":
    db.create_all()
    app.run()


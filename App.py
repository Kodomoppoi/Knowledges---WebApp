from sqlalchemy import create_engine, String, Integer, Column
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///minhabase.sqlite3'
db = SQLAlchemy(app)
app.app_context().push()

#criação da db com sql alchemy

#padrão criacional - Singleton, salvando as bases das opções opcionais
class Topic_Template:
   __instance = None

   def __new__(cls):
       if Topic_Template.__instance is None:
          Topic_Template.__instance = super().__new__(cls)
       return Topic_Template.__instance

   def __init__(self):
       # Atributos de exemplo
       self.complexity = 50
       self.topic_type = "standart"

#decorator será utilizado para adicionar o "topic_type" no topic_1 e topic_2 e sua complexidade
class Fuse_Topics:
    def extractdata(self):
        self.x = x
    
    def getdata(self):
        return self.x
class AddExtra:
    def __init__(self, Fuse_Topics):
        self._Fuse_Topics = Fuse_Topics

    def Type(self):
        self.type = type

    def addComplexity():
        self.complexity = complexity



#criação da db
class Users(db.Model):
    __tablename__ = "users"

    #a db de cada usuario consistirá em  integer {{id}} único, string {{username}}, string {{topic_1}}, string {{topic_2}},integer {{complexity}}, string{{topic_type}}
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique = True, nullable = False)
    topic_1 = db.Column(db.String, nullable = False)
    topic_2 = db.Column(db.String, nullable = False)
    complexity = db.Column(db.Integer)

    def __init__(self, id, username, topic_1, topic_2, complexity):
        self.id = id
        self.username = username
        self.topic_1 = topic_1
        self.topic_2 = topic_2
        self.complexity = complexity

#criação do back-end da pagina index, dar request e guardar na db criada

@app.route('/', methods=['GET', 'POST'])

def addUser():
    if request.method == 'GET':      
        return render_template('index.html')
    elif request.method == 'POST':

        username = request.form.get('username')
        secret_key = request.form.get('senha')
        topic_1 = request.form.get('topic_1')
        topic_2 = request.form.get('topic_2')
        complex_1 = request.form.get('complex_1')
        complex_2 = request.form.get('complex_2')
        type_1 = request.form.get('type_1')
        type_2 = request.form.get('type_2')

        if username == 'LUPO':
            return "acertou o nome"
        else:
            return "NOOO!😡"

        return render_template('index.html')
        

    return "nem entro no metodokkkkk otario"


        





if __name__ == "__main__":
    db.create_all()
    app.run(host = '0.0.0.0', debug = True)


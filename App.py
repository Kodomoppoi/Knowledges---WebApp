from sqlalchemy import create_engine, String, Integer, Column
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///minhabase.sqlite3'
db = SQLAlchemy(app)
app.app_context().push()
app.secret_key = 'KEMSDA'


#padrão criacional - Singleton, salvando as bases das opções opcionais

#criação da db
class Users(db.Model):
    __tablename__ = "Users"

    #a db de cada usuario consistirá em  integer {{id}} único, string {{username}}, string {{topic_1}}, string {{topic_2}},integer {{complexity}}, string{{topic_type}}
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False)
    topic_1 = db.Column(db.String, nullable = False)
    type_1 = db.Column(db.String)
    complex_1 = db.Column(db.Integer)
    topic_2 = db.Column(db.String, nullable = False)
    type_2 = db.Column(db.String)
    complex_2 = db.Column(db.Integer)

    def __init__(self, username, topic_1, topic_2, complex_1, complex_2, type_1, type_2):
        self.username = username
        self.topic_1 = topic_1
        self.topic_2 = topic_2
        self.complex_1= complex_1
        self.complex_2 = complex_2
        self.type_1=type_1
        self.type_2=type_2

#criação do back-end da pagina index, dar request e guardar na db criada

@app.route('/', methods=['GET', 'POST'])

def addUser():

    if request.method == 'GET':      
        return render_template('index.html')
    elif request.method == 'POST':

        username = request.form.get('username')
        topic_1 = request.form.get('topic_1')
        topic_2 = request.form.get('topic_2')
        complex_1 = request.form.get('complex_1')
        complex_2 = request.form.get('complex_2')
        type_1 = request.form.get('type_1')
        type_2 = request.form.get('type_2')
        user = Users(username = username, topic_1=topic_1, topic_2=topic_2, complex_1=complex_1, complex_2=complex_2,type_1=type_1,type_2=type_2)
        db.session.add(user)
        db.session.commit()
        #se a senha for igual, pula o codigo e entra direta
        session['id'] = user.id
        #fazer um if para aceitar uma chave unicas
        return render_template('confirmation.html', user=user)
    
        
@app.route('/confirmation/<id>', methods = ['GET', 'POST'])
def attInfo(id):

    user = Users.query.filter(Users.id == id).first()
    if request.method == 'GET':
        return render_template('confirmation.html', user=user)
    elif request.method == 'POST':

        user.username = request.form.get('username')
        user.topic_1 = request.form.get('topic_1')
        user.topic_2 = request.form.get('topic_2')   
        user.complex_1 = request.form.get('complex_1')
        user.complex_2 = request.form.get('complex_2')
        user.type_1 = request.form.get('type_1')
        user.type_2 = request.form.get('type_2')
        db.session.commit()
        return render_template('confirmation.html', user=user, message = 'informações atualizadas')

        

        





if __name__ == "__main__":
    db.create_all()
    app.run(host = '0.0.0.0', debug = True)


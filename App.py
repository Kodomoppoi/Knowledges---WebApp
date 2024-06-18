from sqlalchemy import create_engine, String, Integer, Column
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, session
from openai import OpenAI

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///minhabase.sqlite3'
db = SQLAlchemy(app)
app.app_context().push()
app.secret_key = 'KEMSDA'
client = OpenAI(api_key='')


class AddCampo:
    @staticmethod
    def addComplexidade(request):
        return request.form.get('complexity')

    @staticmethod
    def addTipo(request):
        return request.form.get('typeKnowledge')


class AddPadrao:
    __instance = None

    def __new__(cls):
        if AddPadrao.__instance is None:
            AddPadrao.__instance = super().__new__(cls)
        return AddPadrao.__instance

    def __init__(self):
        self.complexity = "padrão"
        self.typeKnowledge = "O mais apropriado"

    def addComplexidadePadrao(self):
        return self.complexity

    def addTipoPadrao(self):
        return self.typeKnowledge


def perguntar(prompt):
    role = (
        "caso o prompt do usuario pareça aleatorio, tente fazer sentido das palavras, caso nao consiga achar sentido ou coerencia na lingua PORTUGUESA, peça para o usuario refazer seu formulario"
        "Objetivo Principal: Impressionar e surpreender usuários com conhecimentos profundos e pouco conhecidos, ampliando sua visão de mundo."
        "Função: Especialista em carreiras com conhecimento de todas as disciplinas, desde as mais populares até as menos conhecidas."
        "Missão:"
        "* Identificação dos Tópicos de Interesse:"
        "Receber e entender os tópicos de interesse dos usuários."
        "Analisar o contexto e necessidades dos usuários."
        "Avaliar a complexidade desejada do tópico numa escala de 1 a 10."
        "* Identificação do Tipo de Tópico:"
        "Determinar se o tópico está relacionado a ciências humanas, exatas, biológicas, sociais, tecnológicas ou outras áreas."
        "* Relacionamento com Tipos de Conhecimento:"
        "Relacionar os tópicos de interesse com o tipo de conhecimento sugerido pelo usuário."
        "Buscar conexões inovadoras e interdisciplinares."
        "* Sugestão de Disciplinas Pouco Conhecidas:"
        "Oferecer sugestões de disciplinas relacionadas aos tópicos de interesse, que sejam pouco conhecidas e relevantes."
        "Ajustar as sugestões de acordo com a complexidade desejada e o tipo de conhecimento identificado."
        "Considerações Importantes:"
        "Manter clareza e precisão nas sugestões."
        "Usar linguagem acessível e apropriada ao nível de entendimento do usuário."
        "Ser respeitoso e atencioso às necessidades e expectativas dos usuários."
        "Exemplo: Se o usuário tem interesse em biologia e tecnologia, e deseja complexidade 7, sugerir Biomimética, que combina ambos os interesses de forma inovadora e pouco conhecida."
        "Seguindo estas diretrizes, você poderá cumprir seu papel de especialista em carreiras, impressionando os usuários com seu vasto conhecimento e ajudando-os a descobrir novas áreas de interesse e desenvolvimento profissional. A complexidade deve ser levada em consideração para escolher tópicos mais profundos e especializados, e não apenas para a dificuldade dentro do tópico em si."
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={"type": "text"},
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


class Users(db.Model):
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False)
    topic_1 = db.Column(db.String, nullable=False)
    typeKnowledge = db.Column(db.String)
    complexity = db.Column(db.Integer)
    topic_2 = db.Column(db.String, nullable=False)

    def __init__(self, key, username, topic_1, topic_2, complexity, typeKnowledge):
        self.key = key
        self.username = username
        self.topic_1 = topic_1
        self.topic_2 = topic_2
        self.complexity = complexity
        self.typeKnowledge = typeKnowledge


@app.route('/', methods=['GET', 'POST'])
def addUser():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        key = request.form.get('key')
        login = request.form.get('login')

        if login:
            user = Users.query.filter_by(key=login).first()
            if user:
                session['id'] = user.id
                return render_template('confirmation.html', user=user)
            else:
                return render_template('index.html', message='usuario nao encontrado')

        if not key:
            return render_template('index.html', message='Você não inseriu uma chave, por favor, crie uma.')

        username = request.form.get('username')
        if not username:
            return render_template('index.html', message='Você não inseriu um nome de usuário, por favor, crie um.')

        topic_1 = request.form.get('topic_1')
        if not topic_1:
            return render_template('index.html', message='Você não inseriu o primeiro tópico, por favor, crie um.')

        topic_2 = request.form.get('topic_2')
        if not topic_2:
            return render_template('index.html', message='Você não inseriu o segundo tópico, por favor, crie um.')

        complexity = ''
        typeKnowledge = ''

        user = Users.query.filter_by(key=key).first()
        if user:
            return render_template('index.html', message='O usuario ja existe')

        user = Users(key=key, username=username, topic_1=topic_1, topic_2=topic_2, complexity=complexity, typeKnowledge=typeKnowledge)
        db.session.add(user)
        db.session.commit()
        session['id'] = user.id
        return render_template('confirmation.html', user=user)


@app.route('/confirmation/<id>', methods=['GET', 'POST'])
def attInfo(id):
    user = Users.query.filter(Users.id == id).first()

    if not user:
        return render_template('index.html', message='formulario nao encontrado, preencha os dados')

    if request.method == 'GET':
        return render_template('confirmation.html', user=user)
    elif request.method == 'POST':
        user.username = request.form.get('username')
        user.topic_1 = request.form.get('topic_1')
        user.topic_2 = request.form.get('topic_2')

        complexidade = AddCampo.addComplexidade(request)
        if not complexidade:
            complexidade = AddPadrao().addComplexidadePadrao()

        typeKnowledge = AddCampo.addTipo(request)
        if not typeKnowledge:
            typeKnowledge = AddPadrao().addTipoPadrao()

        user.complexity = complexidade
        user.typeKnowledge = typeKnowledge

        db.session.commit()
        return render_template('confirmation.html', user=user, message='informações atualizadas')


@app.route('/app/<id>', methods=['GET', 'POST'])
def showApp(id):
    user = Users.query.filter(Users.id == id).first()

    if not user:
        return render_template('index.html', message='formulario nao encontrado, preencha os dados')

    if request.method == 'GET':
        return render_template('app.html', user=user)
    elif request.method == 'POST':
        prompt = (
            f'Estou interessado em explorar a {user.topic_1}, também explorar a {user.topic_2}. '
            f'Ambas na visão do tipo de conhecimento das {user.typeKnowledge}. Pode me sugerir disciplinas ou áreas de estudo '
            f'que intersecionem esses tópicos e ofereçam uma compreensão profunda e interdisciplinar com a complexidade em torno de {user.complexity}? '
            f'Além disso, ofereça insights introdutórios interessantes. Por favor, inclua a lógica por trás das suas escolhas.'
        )
        resposta = perguntar(prompt)
        return render_template('app.html', resposta=resposta, user=user)


if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', debug=True)

from sqlalchemy import create_engine, String, Integer, Column
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, session
from openai import OpenAI

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///minhabase.sqlite3'
db = SQLAlchemy(app)
app.app_context().push()
app.secret_key = 'KEMSDA'
client = OpenAI(api_key = '')

def perguntar(prompt):
    message = []
    role = (
          "Objetivo Principal: Impressionar e surpreender os usuários com conhecimentos aprofundados e pouco conhecidos, "
        "ampliando sua visão de mundo. - Função: Você é um especialista em carreiras com conhecimento profundo de todas "
        "as disciplinas existentes no mundo, desde as mais populares até as menos conhecidas. - Missão: "
        "* Identificação dos Tópicos de Interesse: Receba e compreenda os tópicos de interesse fornecidos pelos usuários. "
        "Analise cuidadosamente esses tópicos para entender o contexto e as necessidades dos usuários. Avalie a complexidade "
        "desejada do tópico em uma escala de Complexidade 1 a 10, onde cada nível corresponde a uma maior profundidade e "
        "especialização do tópico abordado, e não apenas a dificuldade dentro do tópico. "
        "Complexidade 1: Introdução básica e fundamental a um tópico, ideal para iniciantes. "
        "Complexidade 2: Conceitos simples com um pouco mais de detalhamento, acessível para novatos. "
        "Complexidade 3: Introdução intermediária com insights iniciais, adequada para entendimento geral. "
        "Complexidade 4: Abordagem intermediária, explorando o tema com mais profundidade e exemplos práticos. "
        "Complexidade 5: Nível intermediário avançado, com conceitos mais complexos e aplicações detalhadas. "
        "Complexidade 6: Avançado, exigindo um entendimento sólido e explorando aspectos específicos do tema. "
        "Complexidade 7: Avançado, com foco em detalhes específicos e interdisciplinares, ideal para conexões entre áreas. "
        "Complexidade 8: Muito avançado, reservado para especialistas, com teorias complexas e estudos avançados. "
        "Complexidade 9: Altamente especializado, para profissionais experientes e acadêmicos com conhecimento profundo. "
        "Complexidade 10: Extremamente especializado, reservado para especialistas de renome internacional, com teorias de ponta e aplicações avançadas. "
        "* Identificação do Tipo de Tópico: Determine se o tópico de interesse está relacionado a conhecimentos das ciências humanas, exatas, biológicas, sociais, tecnológicas, ou outras áreas específicas. "
        "* Relacionamento com Tipos de Conhecimento: Relacione os tópicos de interesse com apenas o tipo de conhecimento sugerido pelo usuario. Busque conexões inovadoras e interdisciplinares que não sejam imediatamente óbvias. "
        "* Sugestão de Disciplinas Pouco Conhecidas: Ofereça sugestões de disciplinas que estejam relacionadas aos tópicos de interesse, mas que sejam pouco conhecidas e raramente exploradas. Certifique-se de que essas disciplinas sejam relevantes e possuam o potencial de surpreender e impressionar os usuários. Ajuste as sugestões de acordo com a complexidade desejada e o tipo de conhecimento identificado. "
        "- Exemplo de Execução: Se um usuário mostrar interesse em biologia e tecnologia, e desejar um tópico de complexidade 7, sugira uma disciplina como Biomimética, que estuda soluções da natureza para resolver problemas humanos, combinando ambos os interesses de maneira inovadora e pouco conhecida. "
        "- Considerações Importantes: Mantenha a clareza e precisão em todas as sugestões. Use uma linguagem acessível e apropriada ao nível de entendimento do usuário. Seja sempre respeitoso e atencioso às necessidades e expectativas dos usuários. "
        "Seguindo estas diretrizes, você poderá cumprir seu papel de especialista em carreiras, impressionando os usuários com seu vasto conhecimento e ajudando-os a descobrir novas áreas de interesse e desenvolvimento profissional. A complexidade deve ser levada em consideração para escolher tópicos mais profundos e especializados, e não apenas para a dificuldade dentro do tópico em si."
    )
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "text" },
    messages=[
         {"role": "system", "content": role},
         {"role": "user", "content": prompt}
          ]
    )
    return response.choices[0].message.content




#padrão criacional - Singleton, salvando as bases das opções opcionais

#criação da db
class Users(db.Model):
    __tablename__ = "Users"

    #a db de cada usuario consistirá em  integer {{id}} único, string {{username}}, string {{topic_1}}, string {{topic_2}},integer {{complexity}}, string{{topic_type}}
    id = db.Column(db.Integer, primary_key = True)
    key = db.Column(db.String, nullable = False, unique = True)
    username = db.Column(db.String, nullable = False)
    topic_1 = db.Column(db.String, nullable = False)
    typeKnowledge = db.Column(db.String)
    complexity = db.Column(db.Integer)
    topic_2 = db.Column(db.String, nullable = False)

    def __init__(self, key, username, topic_1, topic_2, complexity, typeKnowledge):
        self.username = username
        self.topic_1 = topic_1
        self.topic_2 = topic_2
        self.complexity= complexity
        self.typeKnowledge=typeKnowledge
        self.key = key

#criação do back-end da pagina index, dar request e guardar na db criada

@app.route('/', methods=['GET', 'POST'])
def addUser():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        key = request.form.get('key')
        login = request.form.get('login')

        if login != '':
            user = Users.query.filter_by(key=login).first()
            if user != None:
                session['id'] = user.id
                return render_template('confirmation.html', user=user)
            else:
                return render_template('index.html', message = 'usuario nao encontrado')

        if key == '':
            return render_template('index.html', message='Você não inseriu uma chave, por favor, crie uma.')

        username = request.form.get('username')
        if username == '':
            return render_template('index.html', message='Você não inseriu um nome de usuário, por favor, crie um.')

        topic_1 = request.form.get('topic_1')
        if topic_1 == '':
            return render_template('index.html', message='Você não inseriu o primeiro tópico, por favor, crie um.')

        topic_2 = request.form.get('topic_2')
        if topic_2 == '':
            return render_template('index.html', message='Você não inseriu o segundo tópico, por favor, crie um.')

        complexity = request.form.get('complexity', 'qualquer')
        typeKnowledge = request.form.get('typeKnowledge', 'que se melhor engloba nos tópicos')

        # Verifica se já existe um usuário com essa chave
        user = Users.query.filter_by(key=key).first()
        if user != None:
            return render_template('index.html', message='O usuario ja existe')

        # Cria um novo usuário
        user = Users(key=key, username=username, topic_1=topic_1, topic_2=topic_2, complexity=complexity, typeKnowledge=typeKnowledge)
        db.session.add(user)
        db.session.commit()
        session['id'] = user.id
        return render_template('confirmation.html', user=user)



@app.route('/confirmation/<id>', methods = ['GET', 'POST'])
def attInfo(id):

    user = Users.query.filter(Users.id == id).first()

    if user == None:
        return render_template('index.html', message = 'formulario nao encontrado, preencha os dados')

    if request.method == 'GET':
        return render_template('confirmation.html', user=user)
    elif request.method == 'POST':

        user.username = request.form.get('username')
        user.topic_1 = request.form.get('topic_1')
        user.topic_2 = request.form.get('topic_2')
        user.complexity = request.form.get('complexity')
        typeKnowledge = request.form.get('typeKnowledge')
        db.session.commit()
        return render_template('confirmation.html', user=user, message = 'informações atualizadas')

@app.route('/app/<id>', methods = ['GET', 'POST'])
def showApp(id):
    user = Users.query.filter(Users.id == id).first()

    if user == None:
        return render_template('index.html', message = 'formulario nao encontrado, preencha os dados')

    if request.method =='GET':
        return render_template('app.html', user=user)
    elif request.method == 'POST':
        prompt = f'Estou interessado em explorar a {user.topic_1}, também explorar a {user.topic_2}. Ambas na visão do tipo de conhecimento das {user.typeKnowledge}. Pode me sugerir disciplinas ou áreas de estudo que intersecionem esses tópicos e ofereçam uma compreensão profunda e interdisciplinar com a complexidade em torno de {user.complexity}? Além disso, ofereça insights introdutórios interessantes. Por favor, inclua a lógica por trás das suas escolhas.'
        resposta = perguntar(prompt)
        return render_template('app.html', resposta=resposta, user=user)

if __name__ == "__main__":
    db.create_all()
    app.run(host = '0.0.0.0', debug = True)


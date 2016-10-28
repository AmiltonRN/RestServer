import json, requests, xml.etree.ElementTree as etree
import mysql.connector as mysql
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy as SQL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@127.0.0.1/brasil'
db = SQL(app)

response = requests.get("http://www.camara.leg.br/SitCamaraWS/Deputados.asmx/ObterDeputados")
columns = ('id', 'nome', 'matricula', 'partido', 'condicao', 'urlFoto')

class Deputado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80))
    matricula = db.Column(db.String(80))
    partido = db.Column(db.String(80))
    urlFoto = db.Column(db.String(160))
    condicao = db.Column(db.String(80))

    def __init__(self, nome, matricula, partido, urlFoto, condicao):
        self.nome = nome
        self.matricula = matricula
        self.partido = partido
        self.urlFoto = urlFoto
        self.condicao = condicao

    def __toJson__(self):
        return dict(zip(columns, (self.id, self.nome, self.matricula, self.partido, self.urlFoto, self.condicao)))


@app.route('/')
def all():
    db.drop_all()
    db.create_all()
    return 'Hello Word'


@app.route('/deputados/save', methods=['GET'])
def api_deputadosSave():
    if response.status_code == 200:
        try:
            for child in etree.fromstring(response.content).getiterator("deputado"):
                db.session.add(Deputado(child.find('nome').text, child.find('matricula').text,
                                          child.find('partido').text, child.find('urlFoto').text,
                                          child.find('condicao').text))
            db.session.commit()
        except mysql.Error as e:
            print(e)

    return "Found"


@app.route('/deputados/get', methods=['GET'])
def api_deputadosGet():
    results = []
    for row in db.session.query(Deputado).all():
        results.append(row.__toJson__())
    return json.dumps(results)

if __name__ == '__main__':
    app.run(port=5003, debug=True, threaded=True, host='0.0.0.0')

# import json
import requests
import xml.etree.ElementTree as etree

# from flask import Flask, url_for
# app = Flask(__name__)

class Deputado(object):
    
    def __init__(self, nome, matricula, partido, urlFoto, condicao):
        self._nome = nome;
        self._matricula = matricula;
        self._partido = partido;
        self._urlFoto = urlFoto;
        self._condicao = condicao;


    def getNome(self):
        return self._nome
    def getMatricula(self):
        return self._matricula
    def getPartido(self):
        return self._partido
    def getUrlFoto(self):
        return self._urlFoto
    def getCondicao(self):
        return self._condicao

# @app.route('/')
def api_root():
    response = requests.get("http://www.camara.leg.br/SitCamaraWS/Deputados.asmx/ObterDeputados")
    nome = []
    d = []
    matricula = []
    if (response.status_code == 200):
        # comments = json.loads(response.content)
        # print(comments[0]['body'])
        # return (response.content)
        tree = etree.fromstring(response.content)
        links = tree.getiterator("deputado")
        # root = tree.getroot();
        i = 0

        for child in links:
            d.append(Deputado(child.find('nome').text,
                              child.find('matricula').text,
                              child.find('partido').text,
                              child.find('urlFoto').text,
                              child.find('condicao').text))

            # nome.append(child.find('nome').text)
            # matricula.append(child.find('matricula').text)

        for tmp in d:
            print(i+1,tmp.getNome(), tmp.getMatricula(), tmp.getPartido(), tmp.getCondicao())
            i = i + 1
        # print(nome)
        # print(matricula)
    else:
        print("not found")

def api_server():
    response = requests.get("http://127.0.0.1:5000/deputados")
    print(response.content)

if __name__ == '__main__':
    # api_root()
    # app.run()
    api_server()

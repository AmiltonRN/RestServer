import json, requests, xml.etree.ElementTree as etree
import mysql.connector as mysql
import json
from flask import Flask

app = Flask(__name__)

response = requests.get("http://www.camara.leg.br/SitCamaraWS/Deputados.asmx/ObterDeputados")


class Deputado(object):
    def __init__(self, nome, matricula, partido, urlFoto, condicao):
        self._nome = nome
        self._matricula = matricula
        self._partido = partido
        self._urlFoto = urlFoto
        self._condicao = condicao


def jdefault(object):
    return object.__dict__


def open_connect():
    print("Conexao estabelecida")
    return mysql.connect(database="brasil", user="root", password="", host="127.0.0.1")


def save(deputados):
    try:
        conn = open_connect()
        if conn.is_connected():
            c = conn.cursor()
            for deputado in deputados:
                query = "INSERT INTO deputados VALUES(0, %s, %s, %s, %s, %s)"
                args = (deputado._nome, deputado._matricula,
                        deputado._partido, deputado._urlFoto,
                        deputado._condicao)
                c.execute(query, args)
            conn.commit()
            conn.close()
        else:
            print("Conexao falhou")

    except mysql.Error as e:
        print(e)


@app.route('/deputados/save', methods=['GET'])
def api_deputadosSave():
    deputados = []
    if response.status_code == 200:
        for child in etree.fromstring(response.content).getiterator("deputado"):
            deputados.append(Deputado(child.find('nome').text, child.find('matricula').text,
                                      child.find('partido').text, child.find('urlFoto').text,
                                      child.find('condicao').text))
        save(deputados)
    return "Found"


@app.route('/deputados/get', methods=['GET'])
def api_deputadosGet():
    conn = open_connect()
    c = conn.cursor()
    c.execute("SELECT id, nome,  partido, urlFoto, condicao FROM deputados")
    return str(len(json.dumps(c.fetchall())))
    # table = "<center><table border=1><tr><th>id</th><th>Nome</th><th>Partido</th><th>Foto</th><th>Condicao</th></tr>"
    # for row in c.fetchall():
    #     table = table + '<tr><td>' + str(row[0]) + '</td><td>'
    #     table = table + row[1] + "</td><td>"
    #     table = table + row[2] + "</td><td><a href = "
    #     table = table + row[3] + "> Veja a Foto do Elemento(A) </a></td><td>"
    #     table = table + row[4] + "</tr></td>"
    # return table + "</table></center>"


# @app.route('/deputadosJson', methods=['GET'])
# def api_deputadosJson():
#     deputados = []
#     if response.status_code == 200:
#         for child in etree.fromstring(response.content).getiterator("deputado"):
#             deputados.append(Deputado(child.find('nome').text,
#                                       child.find('matricula').text,
#                                       child.find('partido').text,
#                                       child.find('urlFoto').text,
#                                       child.find('condicao').text))
#         return (json.dumps(deputados, default=jdefault))
#     else:
#         return "not found"
#
#
# @app.route('/deputadosXml', methods=['GET'])
# def api_deputadosXml():
#     # response = requests.get("http://www.camara.leg.br/SitCamaraWS/Deputados.asmx/ObterDeputados")
#     deputados = []
#     if response.status_code == 200:
#         table = "<center><table border=1><tr><th>Nome</th><th>Partido</th><th>Foto</th><th>Condicao</th></tr>"
#         for child in etree.fromstring(response.content).getiterator("deputado"):
#             table = table + "<tr><td>" + child.find('nome').text + "</td><td>"
#             table = table + child.find('partido').text + "</td><td><a href = "
#             table = table + child.find('urlFoto').text + "> Veja a Foto do Elemento(A) </a></td><td>"
#             table = table + child.find('condicao').text + "</tr></td>"
#         return table + "</table></center>"
#     else:
#         return "not found"


if __name__ == '__main__':
    app.run(host='localhost', port=5002)
    # connect()

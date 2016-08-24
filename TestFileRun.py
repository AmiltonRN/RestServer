import subprocess as sp
import os
import re
import json
from string import upper

from flask import Flask

app = Flask(__name__)

columns = ('posicao','proximidade','nome')


@app.route('/pharmer/find/<pharmacophore>', methods=['GET'])
def runFile(pharmacophore):
    f = open('tmpFile.query', 'w')  # grava o arquivo de entrada no diretorio
    f.write(pharmacophore)
    f.close()
    os.system('./pharmer.ubuntu.12.04 dbsearch -dbdir /home/amilton/ATUAL -in tmpFile.query -out saida.txt')

    result = []
    for linha in open('saida.txt', 'r').readlines():
        tmp = re.split(r'[;,\s]\s*', upper(linha))
        result.append({columns[0]: int(tmp[0]), columns[1]: float(tmp[1]), columns[2]: tmp[4]})

    return json.dumps(result)  # pegar o saida.txt e converter para json;


if __name__ == '__main__':
    app.run(host='0.0.0.0')
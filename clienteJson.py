import requests
from flask import jsonify
import server


def app_convert():
    response = requests.get("http://localhost:5000/deputadosJson")
    deputados = jsonify(results=response.content)
    print (deputados)


if __name__ == '__main__':
    app_convert()

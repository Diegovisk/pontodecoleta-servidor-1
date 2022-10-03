from time import time
from flask import Flask, request
from flask_cors import CORS
from database.queries import (
    get_caixas,
    get_capacidades,
    get_coletas,
    get_doacoes,
    insert_capacidade,
    insert_doacao,
)

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return "Hello, doações!"


@app.post("/doacao/<int:id_caixa>")
def doacao(id_caixa):
    doacao = request.form["doacao"]
    insert_doacao(doacao, id_caixa)
    return "OK"


# Register coleta
@app.post("/coleta/<int:id_caixa>")
def coleta(id_caixa):
    coleta(id_caixa)
    return "OK"


# Register capacidade
@app.post("/capacidade/<int:id_caixa>")
def capacidade(id_caixa):
    centimetros = request.form["capacidade"]
    insert_capacidade(centimetros, id_caixa)
    return "OK"


# get caixa capacidades
@app.get("/caixa/<int:id_caixa>/capacidades")
def caixa_capacidades(id_caixa):
    inicio = request.args.get("inicio")
    fim = request.args.get("fim")

    if inicio.isdigit():
        inicio = int(inicio)
    else:
        inicio = 0

    if fim.isdigit():
        fim = int(fim)
    else:
        fim = int(time())

    return get_capacidades(id_caixa, inicio, fim)


# Get all caixas
@app.get("/caixas")
def caixas():
    return get_caixas()


# Get caixas collects
@app.get("/caixa/<int:id_caixa>/coletas")
def coletas(id_caixa):
    coletas = get_coletas(id_caixa)
    coletas = (
        [{"id": 0, "timestamp": "Criação"}]
        + coletas
        + [{"id": 0, "timestamp": "Agora"}]
    )
    intervalos = []
    for i in range(len(coletas) - 1):
        intervalos.append(
            {
                "id": coletas[i]["id"],
                "inicio": coletas[i]["timestamp"],
                "fim": coletas[i + 1]["timestamp"],
            }
        )
    return intervalos


# Get caixa donations
@app.get("/caixa/<int:id_caixa>/doacoes")
def doacoes(id_caixa):
    inicio = request.args.get("inicio")
    fim = request.args.get("fim")

    if inicio.isdigit():
        inicio = int(inicio)
    else:
        inicio = 0

    if fim.isdigit():
        fim = int(fim)
    else:
        fim = 9999999999

    print(inicio, fim)

    return get_doacoes(id_caixa, inicio, fim)


if __name__ == "__main__":
    app.run(host="0.0.0.0")

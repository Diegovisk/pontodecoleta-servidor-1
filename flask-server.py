from flask import Flask

from database.queries import insert_capacidade, insert_doacao
from flask import request

app = Flask(__name__)

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

# Get all caixas
@app.get("/caixas")
def caixas():
    

if __name__ == "__main__":
    app.run()
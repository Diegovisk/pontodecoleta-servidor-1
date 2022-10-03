from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.post("/doacao")
def doacao():
    
    return "Doação recebida!"
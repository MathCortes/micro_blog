import datetime
import os
import certifi
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    '''
    Não é uma boa pratica criar a conexão com o banco de dados MongoDatabase
    Quando acontece o mecanismo de deploy, esse arquivo pode ser executado multiplas vezes gerando um processamento desnecessário
    O que acontece na pratica é a criação de vários objetos "client" atrvés da execução múltipla do MongoClient()
    '''
    app = Flask(__name__)
    app.config['DEBUG'] = True

    # Conectando com o MongoDatabase
    ca = certifi.where()
    client = MongoClient(os.getenv("MONGODB_URI"), tlsCAFile=ca)
    app.db = client.microblog

    @app.route("/", methods=["GET", "POST"])
    def home():

        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            
            app.db.entries.insert_one({"content":entry_content, "date":formatted_date})

        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]

        return render_template("home.html", entries=entries_with_date)

    if __name__ == "__main__":
        app.run(debug=True)
    
    return app

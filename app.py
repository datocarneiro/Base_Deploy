# Add these at the top of your settings.py
from os import getenv
from dotenv import load_dotenv
import psycopg2
from flask import Flask, render_template, request, redirect, url_for
import os

load_dotenv()
# Parâmetros de conexão com o banco de dados PostgreSQL
dbname = getenv('PGDATABASE')
user = getenv('PGUSER')
password = getenv('PGPASSWORD')
host = getenv('PGHOST')
port = getenv('PGPORT')
connection_url = getenv('CONECTION_URL')

app = Flask(__name__)
@app.route("/")
def create_connection():
    try:
        conexao = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )


        
        # # Conectando ao banco de dados usando a URL
        # conexao = psycopg2.connect(connection_url)


        mensagem="Conexão com o banco de dados bem-sucedida"
        print(mensagem)
        conexao.close() # fecha conexão
        return mensagem
    
    except psycopg2.Error as e:
        mensagem=f"Erro ao conectar ao BANCO DE DADOS:........\n , {e}"
        print(mensagem)
        return mensagem

# Testando a conexão
conexao = create_connection()


if __name__ == '__main__':
    # # Ativa o modo de depuração para reiniciar automaticamente o servidor em caso de alterações no código
    # port = int(os.getenv('PORT', 10000))  # Use a porta definida pela variável de ambiente PORT, ou 9090 se não estiver definida
    app.run(host='0.0.0.0', port=9090)
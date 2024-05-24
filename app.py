import psycopg2
from psycopg2 import OperationalError
from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
from dotenv import load_dotenv

load_dotenv()

# Parâmetros de conexão com o banco de dados PostgreSQL
dbname = os.getenv('PGDATABASE')
user = os.getenv('PGUSER')
password = os.getenv('PGPASSWORD')
host = os.getenv('PGHOST')
port = os.getenv('PGPORT')
connection_url = os.getenv('CONNECTION_URL')

app = Flask(__name__)

def create_connection():
    try:
        conexao = psycopg2.connect(connection_url)
        print("Conexão com o banco de dados bem-sucedida")
        return conexao, e
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao BANCO DE DADOS: {e}")
        return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_table")
def create_table():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tabelaBd (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(100),
                    posicao VARCHAR(100),
                    nivel VARCHAR(100),
                    status VARCHAR(100)
                );
            """)
            conn.commit()
            cursor.close()
            conn.close()
            return "Tabela criada com sucesso!"
        except psycopg2.Error as e:
            return f"Erro ao criar a tabela: {e}"
    return "Falha na conexão com o banco de dados."

@app.route("/insert", methods=["GET", "POST"])
def insert():
    if request.method == "POST":
        nome = request.form["nome"]
        posicao = request.form["posicao"]
        nivel = request.form["nivel"]
        status = request.form["status"]
        
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO tabelaBd (nome, posicao, nivel, status) VALUES (%s, %s, %s, %s);
                """, (nome, posicao, nivel, status))
                conn.commit()
                cursor.close()
                conn.close()
                return redirect(url_for('index'))
            except psycopg2.Error as e:
                return f"Erro ao inserir dados: {e}"
        return "Falha na conexão com o banco de dados."
    return render_template("insert.html")

@app.route("/select")
def select():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tabelaBd;")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template("select.html", rows=rows)
        except psycopg2.Error as e:
            return f"Erro ao consultar dados: {e}"
    return "Falha na conexão com o banco de dados."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)

from flask import Blueprint, render_template, request, redirect
from models.models import listar_alunos
from extensions import mysql

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return render_template('base.html')

@routes.route('/alunos', methods=['GET', 'POST'])
def alunos():
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        try:
            nome = request.form['nome']
            data_nasc = request.form['data_nascimento']
            email = request.form['email']
            telefone = request.form['telefone']
            
            cur.execute("""
                INSERT INTO alunos (nome, data_nascimento, email, telefone)
                VALUES (%s, %s, %s, %s)
            """, (nome, data_nasc, email, telefone))
            mysql.connection.commit()
            return redirect('/alunos')
        
        except Exception as e:
            mysql.connection.rollback()
            print(f"Erro ao inserir aluno: {e}")
            return "Erro ao salvar aluno", 500

    # Consulta os alunos
    cur.execute("SELECT * FROM alunos")
    alunos = cur.fetchall()
    colunas = [desc[0] for desc in cur.description]
    lista_alunos = [dict(zip(colunas, linha)) for linha in alunos]
    
    return render_template('alunos.html', alunos=lista_alunos)


@routes.route('/treinos', methods=['GET', 'POST'])
def treinos():
    cur = mysql.connection.cursor()

    if request.method == "POST":
        aluno_id = request.form["aluno_id"]
        treinador_id = request.form["treinador_id"]
        descricao = request.form["descricao"]
        data_treino = request.form["data_treino"]
        cur.execute("""
            INSERT INTO treinos (aluno_id, treinador_id, descricao, data_treino)
            VALUES (%s, %s, %s, %s)
        """, (aluno_id, treinador_id, descricao, data_treino))
        mysql.connection.commit()
        return redirect("/treinos")

    # Buscar alunos
    cur.execute("SELECT id, nome FROM alunos")
    alunos = cur.fetchall()

    # Buscar treinadores
    cur.execute("SELECT id, nome FROM treinadores")
    treinadores = cur.fetchall()

    # Buscar treinos (com nome do aluno e do treinador)
    cur.execute("""
        SELECT t.id, a.nome AS aluno_nome, tr.nome AS treinador_nome, t.descricao, t.data_treino
        FROM treinos t
        JOIN alunos a ON t.aluno_id = a.id
        JOIN treinadores tr ON t.treinador_id = tr.id
        ORDER BY t.data_treino DESC
    """)
    treinos = cur.fetchall()

    cur.close()
    return render_template("treinos.html", alunos=alunos, treinadores=treinadores, treinos=treinos)

@routes.route('/treinadores', methods=['GET', 'POST'])
def treinadores():
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        nome = request.form['nome']
        especialidade = request.form['especialidade']
        cur.execute("INSERT INTO treinadores (nome, especialidade) VALUES (%s, %s)", (nome, especialidade))
        mysql.connection.commit()
        return redirect('/treinadores')
    
    cur.execute("SELECT * FROM treinadores")
    treinadores = cur.fetchall()
    colunas = [desc[0] for desc in cur.description]
    lista_treinadores = [dict(zip(colunas, linha)) for linha in treinadores]

    cur.close()
    return render_template("treinadores.html", treinadores=lista_treinadores)

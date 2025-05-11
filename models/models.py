def listar_alunos(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM alunos")
    alunos = cur.fetchall()
    cur.close()
    return alunos

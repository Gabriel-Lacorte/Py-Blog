from mysql.connector import connect

config = {
    'host': '',
    'user': '',
    'password': '',
    'database': ''
}

def obter_todos_posts():
    with connect(**config) as db:
        cursor = db.cursor()
        cursor.execute('SELECT id, title, content, author FROM Posts')
        return cursor.fetchall()

def obter_post_por_id(post_id):
    with connect(**config) as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM Posts WHERE id = %s', (post_id,))
        return cursor.fetchall()

def inserir_post(title, content, author):
    with connect(**config) as db:
        cursor = db.cursor()
        sql = "INSERT INTO Posts (title, content, author) VALUES (%s, %s, %s)"
        valores = (title, content, author)
        cursor.execute(sql, valores)
        db.commit()

def excluir_post_por_id(post_id):
    with connect(**config) as db:
        cursor = db.cursor()
        cursor.execute('DELETE FROM Posts WHERE id = %s', (post_id,))
        db.commit()

def obter_comentarios_por_post_id(post_id):
    with connect(**config) as db:
        cursor = db.cursor()
        cursor.execute('SELECT content, author FROM Comments WHERE postid = %s', (post_id,))
        return cursor.fetchall()

def inserir_comentario(content, author, post_id):
    with connect(**config) as db:
        cursor = db.cursor()
        sql = 'INSERT INTO Comments (content, author, postid) VALUES (%s, %s, %s)'
        valores = (content, author, post_id)
        cursor.execute(sql, valores)
        db.commit()

def obter_usuario_por_nome(usuario):
    with connect(**config) as db:
        cursor = db.cursor()
        cursor.execute('SELECT id, user, password FROM Users WHERE user = %s', (usuario,))
        return cursor.fetchone()

def inserir_usuario(usuario, senha_hash):
    with connect(**config) as db:
        cursor = db.cursor()
        sql = "INSERT INTO Users (user, password) VALUES (%s, %s)"
        valores = (usuario, senha_hash)
        cursor.execute(sql, valores)
        db.commit()

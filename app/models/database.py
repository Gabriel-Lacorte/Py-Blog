#from sqlite3 import connect
from mysql.connector import connect

db = connect()
cursor = db.cursor()

def obter_todos_posts():
    cursor.execute('SELECT id, title, content, author FROM Posts')
    return cursor.fetchall()

def obter_post_por_id(post_id):
    cursor.execute('SELECT * FROM Posts WHERE id = ?', (post_id,))
    return cursor.fetchall()

def inserir_post(title, content, author):
    sql = "INSERT INTO Posts (title, content, author) VALUES (?, ?, ?)"
    valores = (title, content, author)
    cursor.execute(sql, valores)
    db.commit()

def excluir_post_por_id(post_id):
    cursor.execute('DELETE FROM Posts WHERE id = ?', (post_id,))
    db.commit()

def obter_comentarios_por_post_id(post_id):
    cursor.execute('SELECT content, author FROM Comments WHERE postid = ?', (post_id,))
    return cursor.fetchall()

def inserir_comentario(content, author, post_id):
    sql = 'INSERT INTO Comments (content, author, postid) VALUES (?, ?, ?)'
    valores = (content, author, post_id)
    cursor.execute(sql, valores)
    db.commit()

def obter_usuario_por_nome(usuario):
    cursor.execute('SELECT id, user, password FROM Users WHERE user = ?', (usuario,))
    return cursor.fetchone()

def inserir_usuario(usuario, senha_hash):
    sql = "INSERT INTO Users (user, password) VALUES (?, ?)"
    valores = (usuario, senha_hash)
    cursor.execute(sql, valores)
    db.commit()

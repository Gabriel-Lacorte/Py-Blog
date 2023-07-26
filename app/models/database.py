from mysql.connector import connect

# Configurações do banco de dados (host, usuário, senha e nome do banco de dados).
config = {
    'host': '',       # Endereço do servidor do banco de dados
    'user': '',       # Nome de usuário do banco de dados
    'password': '',   # Senha do banco de dados
    'database': ''    # Nome do banco de dados a ser utilizado
}

# Função para obter todos os posts do banco de dados.
def obter_todos_posts():
    with connect(**config) as db:
        cursor = db.cursor()
        cursor.execute('SELECT id, title, content, author FROM Posts')
        return cursor.fetchall()

# Função para obter um post específico com base no ID do post.
def obter_post_por_id(post_id):
    with connect(**config) as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM Posts WHERE id = %s', (post_id,))
        return cursor.fetchall()

# Função para inserir um novo post no banco de dados.
def inserir_post(title, content, author):
    with connect(**config) as db:
        cursor = db.cursor()
        sql = "INSERT INTO Posts (title, content, author) VALUES (%s, %s, %s)"
        valores = (title, content, author)
        cursor.execute(sql, valores)
        db.commit()

# Função para excluir um post com base no ID do post.
def excluir_post_por_id(post_id):
    with connect(**config) as db:
        cursor = db.cursor()
        cursor.execute('DELETE FROM Posts WHERE id = %s', (post_id,))
        db.commit()

# Função para obter todos os comentários de um post específico com base no ID do post.
def obter_comentarios_por_post_id(post_id):
    with connect(**config) as db:
        cursor = db.cursor()
        cursor.execute('SELECT content, author FROM Comments WHERE postid = %s', (post_id,))
        return cursor.fetchall()

# Função para inserir um novo comentário em um post no banco de dados.
def inserir_comentario(content, author, post_id):
    with connect(**config) as db:
        cursor = db.cursor()
        sql = 'INSERT INTO Comments (content, author, postid) VALUES (%s, %s, %s)'
        valores = (content, author, post_id)
        cursor.execute(sql, valores)
        db.commit()

# Função para obter um usuário específico com base no nome do usuário.
def obter_usuario_por_nome(usuario):
    with connect(**config) as db:
        cursor = db.cursor()
        cursor.execute('SELECT id, user, password FROM Users WHERE user = %s', (usuario,))
        return cursor.fetchone()

# Função para inserir um novo usuário no banco de dados.
def inserir_usuario(usuario, senha_hash):
    with connect(**config) as db:
        cursor = db.cursor()
        sql = "INSERT INTO Users (user, password) VALUES (%s, %s)"
        valores = (usuario, senha_hash)
        cursor.execute(sql, valores)
        db.commit()

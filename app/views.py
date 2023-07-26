from flask import render_template, redirect, request, session
from app.models import database
from app import app
import bcrypt

# Rota para exibir todos os posts na página inicial, juntamente com o número de comentários em cada post.
@app.route('/', methods=['GET'])
def inicio():
    # Busca todos os posts no banco de dados.
    resultado = database.obter_todos_posts()

    # Para cada post, conta o número de comentários e armazena em quant_comentarios.
    quant_comentarios = {}
    for id, _, _, _, in resultado:
        comentarios = database.obter_comentarios_por_post_id(id)
        quant_comentarios[id] = len(comentarios)

    # Renderiza o template da página inicial com os posts e quant_comentarios como contexto.
    return render_template('inicio.html', posts=resultado, quant_comentarios=quant_comentarios)

# Rota para publicar um novo post ou exibir o formulário de publicação.
@app.route('/publicar', methods=["GET", "POST"])
def publicar():
    # Se o usuário não estiver logado, redireciona-o para a página de login.
    if "id" not in session:
        return redirect('/login')

    # Se o método da solicitação for POST, processa os dados do formulário e insere o post no banco de dados.
    if request.method == "POST":
        titulo = request.form["titulo"].strip()
        conteudo = request.form["conteudo"].strip()
        autor = session['usuario']

        if not titulo or not conteudo:
            return render_template("publicar.html", erro="Preencha todos os campos.")

        if len(titulo) > 200:
            return render_template("publicar.html", erro="O título deve ter no máximo 200 caracteres.")

        if len(conteudo) > 10000:
            return render_template("publicar.html", erro="O conteúdo deve ter no máximo 10000 caracteres.")

        database.inserir_post(titulo, conteudo, autor)

        return redirect('/')

    # Se o método da solicitação for GET, renderiza o formulário de publicação.
    return render_template('publicar.html')

# Rota para exibir um único post e seus comentários.
@app.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    # Busca o conteúdo e os comentários do post com o id fornecido no banco de dados.
    conteudo = database.obter_post_por_id(id)
    comentarios = database.obter_comentarios_por_post_id(id)

    # Renderiza o template do post com o conteúdo e os comentários como contexto.
    return render_template('post.html', conteudo=conteudo, id=id, comentarios=comentarios)

# Rota para excluir um post com um determinado id.
@app.route('/excluir_post/<int:id>')
def excluir_post(id):
    # Se o usuário não estiver logado, redireciona-o para a página de login.
    if 'id' not in session:
        return redirect('/login')

    # Busca o post com o id fornecido no banco de dados.
    post = database.obter_post_por_id(id)

    # Verifica se o post existe e se o usuário atual é o autor do post.
    if post and session['usuario'] == post[0][3]:
        database.excluir_post_por_id(id)

    # Redireciona para a página inicial após a exclusão.
    return redirect('/')

# Rota para postar um comentário em um post específico.
@app.route('/postar_comentario/<int:id>', methods=['GET', 'POST'])
def postar_comentario(id):
    # Se o usuário não estiver logado, redireciona-o para a página de login.
    if "id" not in session:
        return redirect('/login')

    # Se o método da solicitação for POST, processa os dados do formulário e insere o comentário no banco de dados.
    if request.method == 'POST':
        content = request.form['comentario'].strip()
        author = session['usuario'].strip()

        if content and len(content) <= 300:
            database.inserir_comentario(content, author, id)

        return redirect(f'/post/{id}')

# Rota para o login do usuário.
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Se o usuário já estiver logado, redireciona-o para a página inicial.
    if "id" in session:
        return redirect('/')

    # Se o método da solicitação for POST, processa os dados do formulário e verifica as credenciais do usuário.
    if request.method == 'POST':
        usuario = request.form['usuario'].strip()
        senha = request.form['senha'].strip()

        if not usuario or not senha:
            return render_template("login.html", erro="Você deve preencher todos os campos antes de continuar.")

        resultado = database.obter_usuario_por_nome(usuario)

        if resultado and bcrypt.checkpw(senha.encode("utf-8"), resultado[2].encode("utf-8")):
            session["id"] = resultado[0]
            session["usuario"] = resultado[1]
            return redirect("/")

        return render_template("login.html", erro='O usuário ou senha digitado é inválido.')

    # Se o método da solicitação for GET, renderiza a página de login.
    return render_template("login.html")

# Rota para o registro de um novo usuário.
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    # Se o usuário já estiver logado, redireciona-o para a página inicial.
    if "id" in session:
        return redirect('/')

    # Se o método da solicitação for POST, processa os dados do formulário e insere um novo usuário no banco de dados.
    if request.method == "POST":
        usuario = request.form["usuario"].strip()
        senha = request.form["senha"].strip()
        confirmar = request.form["confirmar"].strip()

        if not usuario or not senha or not confirmar:
            return render_template("cadastro.html", erro="Você deve preencher todos os campos antes de continuar.")

        if senha != confirmar:
            return render_template("cadastro.html", erro="As senhas digitadas são diferentes.")

        resposta = database.obter_usuario_por_nome(usuario)

        if resposta:
            return render_template("cadastro.html", erro="O usuário digitado já existe.")

        # Gera o hash da senha e insere o novo usuário no banco de dados.
        hash_senha_encoded = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())
        hash_senha = hash_senha_encoded.decode('utf-8')
        database.inserir_usuario(usuario, hash_senha)

        return redirect("/login")

    # Se o método da solicitação for GET, renderiza o formulário de registro.
    return render_template("cadastro.html")

# Rota para efetuar logout do usuário.
@app.route('/logout')
def logout():
    # Remove as informações do usuário da sessão e redireciona para a página de login.
    session.pop('id', None)
    session.pop('usuario', None)
    return redirect('/login')

# Rota para lidar com erros 404 (página não encontrada).
@app.errorhandler(404)
def nao_encontrada(erro):
    # Renderiza o template 404.html para lidar com a página não encontrada.
    return render_template('404.html')

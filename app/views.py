from flask import render_template, redirect, request, session
from app.models import database
from app import app
import bcrypt

@app.route('/')
def inicio():
    resultado = database.obter_todos_posts()

    quant_comentarios = {}
    for id, _, _, _, in resultado:
        comentarios = database.obter_comentarios_por_post_id(id)
        quant_comentarios[id] = len(comentarios)
    
    return render_template('inicio.html', posts=resultado, quant_comentarios=quant_comentarios)

@app.route('/publicar', methods=["GET", "POST"])
def publicar():
    if "id" not in session:
        return redirect('/login')
        
    if request.method == "POST":
        titulo = request.form["titulo"].strip()
        conteudo = request.form["conteudo"].strip()
        autor = session['usuario']
        
        if not titulo or not conteudo:
            return render_template("publicar.html", erro="Preencha todos os campos.")
        
        if len(titulo) > 200:
            return render_template("publicar.html", erro="O titulo deve ter no máximo 200 caracteres.")
        
        if len(conteudo) > 10000:
            return render_template("publicar.html", erro="O conteúdo deve ter no máximo 10000 caracteres.")

        database.inserir_post(titulo, conteudo, autor)

        return redirect('/')
    
    return render_template('publicar.html')

@app.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    conteudo = database.obter_post_por_id(id)
    comentarios = database.obter_comentarios_por_post_id(id)
    
    return render_template('post.html', conteudo=conteudo, id=id, comentarios=comentarios)

@app.route('/excluir_post/<int:id>')
def excluir_post(id):
    if 'id' not in session:
        return redirect('/login')
    
    post = database.obter_post_por_id(id)
    if post and session['usuario'] == post[0][3]:  # Coloquei [0][3] para acessar o autor do post
        database.excluir_post_por_id(id)
    
    return redirect('/')
    
@app.route('/postar_comentario/<int:id>', methods=['GET', 'POST'])
def postar_comentario(id):
    if "id" not in session:
        return redirect('/login')
        
    if request.method == 'POST':
        content = request.form['comentario'].strip()
        author = session['usuario'].strip()
            
        if content and len(content) <= 300:
            database.inserir_comentario(content, author, id)
            
        return redirect(f'/post/{id}')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if "id" in session:
        return redirect('/')
    
    if request.method == 'POST':
        usuario = request.form['usuario'].strip()
        senha = request.form['senha'].strip()
        
        if not usuario or not senha:
            return render_template("login.html", erro="Você deve preencher todos os campos antes de continuar.")
        
        resultado = database.obter_usuario_por_nome(usuario)
        
        if resultado and bcrypt.checkpw(
            senha.encode("utf-8"), resultado[2].encode("utf-8")
        ):
            session["id"] = resultado[0]
            session["usuario"] = resultado[1]
            return redirect("/")
        
        return render_template("login.html", erro='O usuário ou senha digitado é inválido.')
                
    return render_template("login.html")

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if "id" in session:
        return redirect('/')
    
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

        hash_senha_encoded = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())
        hash_senha = hash_senha_encoded.decode('utf-8')
        database.inserir_usuario(usuario, hash_senha)

        return redirect("/login")

    return render_template("cadastro.html")

@app.route('/logout')
def logout():
    session.pop('id', None)
    session.pop('usuario', None)
    return redirect('/login')

@app.errorhandler(404)
def nao_encontrada(erro):
    return render_template('404.html')

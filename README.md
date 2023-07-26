# 📝 PyBlog - Blog em Python

PyBlog é um blog desenvolvido em Flask que permite aos usuários criarem e compartilharem suas postagens sobre diversos temas. O projeto é simples e flexível, permitindo fácil personalização.

## Funcionalidades

- Visualizar todos os posts na página inicial.
- Publicar novos posts.
- Visualizar detalhes de um post específico.
- Excluir posts (apenas o autor do post tem essa opção).
- Postar comentários em um post.
- Realizar cadastro, login e logout.

## Criando o Banco de Dados

Antes de executar o PyBlog, você precisa criar o banco de dados necessário para armazenar as informações dos posts, comentários e usuários. Para fazer isso, siga os passos abaixo:

1. Abra o seu gerenciador de banco de dados (por exemplo, MySQL Workbench ou phpMyAdmin) e conecte-se ao servidor de banco de dados.

2. Execute o seguinte código SQL para criar o banco de dados:

```sql
CREATE DATABASE IF NOT EXISTS pyblog;
```

3. Em seguida, selecione o banco de dados recém-criado:

```sql
USE pyblog;
```

4. Agora, crie as tabelas necessárias executando os seguintes comandos SQL:

```sql
-- Tabela 'comments'
CREATE TABLE `comments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `content` varchar(256) NOT NULL,
  `author` varchar(256) NOT NULL,
  `postid` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Tabela 'posts'
CREATE TABLE `posts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(256) NOT NULL,
  `content` text NOT NULL,
  `author` varchar(256) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Tabela 'users'
CREATE TABLE `Users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user` varchar(256) NOT NULL,
  `password` varchar(256) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```


## Como executar

Para iniciar o servidor do PyBlog, execute o seguinte comando na raiz do projeto:

```shell
python app.py
```

O servidor estará disponível em http://localhost:5000/.

## Testando online

Você também pode acessar a versão online do PyBlog [clicando aqui](https://lacorte.pythonanywhere.com/).

## Contribuindo

Contribuições são bem-vindas! Se você achou alguma vulnerabilidade ou deseja contribuir para o desenvolvimento do PyBlog, sinta-se à vontade para abrir um problema ou enviar uma solicitação de pull.

## Licença

Este projeto é licenciado sob a Licença MIT.

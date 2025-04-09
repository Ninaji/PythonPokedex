# CVE — SQL Injection em /login

## Descrição

A aplicação Flask permite injeção de código SQL através do campo `usuario` no endpoint `/login`. A falta de sanitização permite que um invasor acesse contas sem fornecer senhas válidas.

## Endpoint vulnerável



## Proof of Concept (PoC)

1. Acesse `http://127.0.0.1:5000/`
2. No campo de **usuário**, insira: `' OR 1=1 --`
3. No campo de **senha**, pode deixar qualquer coisa
4. Você será autenticado como o primeiro usuário do banco de dados

## Impacto

Permite login não autorizado como qualquer usuário, acesso a dados restritos, e potencial acesso à conta de administrador.

## Código vulnerável

	python
query = f"SELECT * FROM dados WHERE user = '{username}'"
user_data = conn.execute(query).fetchone()

Correção: 
query = "SELECT * FROM dados WHERE user = ?"
user_data = conn.execute(query, (username,)).fetchone()

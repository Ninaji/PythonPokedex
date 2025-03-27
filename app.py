from flask import Flask, render_template, redirect, url_for, flash, request, make_response
import sqlite3, requests
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Altere para uma chave secreta real

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Para acessar colunas pelo nome
    return conn

# Modelo de Usuário
class User(UserMixin):
    def __init__(self, id, user, senha, idade):
        self.id = id
        self.user = user
        self.senha = senha
        self.idade = idade

# Carregar o usuário
@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user_data = conn.execute('SELECT * FROM dados WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user_data:
        return User(user_data['id'], user_data['user'], user_data['senha'], user_data['idade'])
    return None

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['usuario']
    password = request.form['senha']
    
    conn = get_db_connection()
    user_data = conn.execute('SELECT * FROM dados WHERE user = ?', (username,)).fetchone()
    conn.close()
    
    if user_data and user_data['senha'] == password:
        user = User(user_data['id'], user_data['user'], user_data['senha'], user_data['idade'])
        login_user(user)

        # Criar um cookie para lembrar o nome do usuário
        resp = make_response(redirect(url_for('dashboard')))  # Criar uma resposta
        resp.set_cookie('username', user.user)  # Definir o cookie
        return resp  # Retornar a resposta com o cookie
    else:
        flash('Usuário ou senha incorretos!')
        return redirect(url_for('home'))

@app.route('/success')
@login_required
def success():
    return render_template('success.html', usuario=current_user.user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/debug')
def debug():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM dados').fetchall()
    conn.close()
    user_list = [(user['id'], user['user'], user['senha'], user['idade']) for user in users]
    return render_template('debug.html', users=user_list)

@app.route('/dashboard')
@login_required
def dashboard():
    username = request.cookies.get('username')  # Obter o cookie
    return render_template('dashboard.html', usuario=username)

@app.route('/pokedex', methods=['GET', 'POST'])
@login_required
def pokedex():
    pokemon_id = request.args.get('id', default=1, type=int)  # Pega o ID do Pokémon da query string
    if request.method == 'POST':
        search_query = request.form.get('search')  # Pega o valor da barra de busca
        if search_query.isdigit():  # Se for um ID
            pokemon_id = int(search_query)
        else:  # Se for um nome
            response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{search_query.lower()}')
            if response.status_code == 200:
                pokemon_id = response.json()['id']
            else:
                flash('Pokémon não encontrado!')
                return redirect(url_for('pokedex'))

    # Busca os dados do Pokémon
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}')
    if response.status_code != 200:
        flash('Pokémon não encontrado!')
        return redirect(url_for('pokedex'))

    pokemon_data = response.json()
    return render_template('pokedex.html', pokemon=pokemon_data)

if __name__ == '__main__':
    app.run(debug=True)
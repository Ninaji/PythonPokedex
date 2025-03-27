import sqlite3

# Nome do banco de dados
DATABASE = 'database.db'

def create_database():
    # Conectar ao banco de dados (ou criar se não existir)
    conn = sqlite3.connect(DATABASE)
    
    # Criar um cursor
    cursor = conn.cursor()
    
    # Criar a tabela
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER NOT NULL
    );
    ''')
    
    # Salvar (commit) as mudanças e fechar a conexão
    conn.commit()
    conn.close()
    print(f"Banco de dados '{DATABASE}' criado com sucesso!")

if __name__ == '__main__':
    create_database()
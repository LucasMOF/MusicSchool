
import mysql.connector

# Conectando ao MySQL
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password=''
)

# Criando um cursor (objeto que executa comandos SQL)
cursor = conexao.cursor()

# Criando o banco de dados
cursor.execute('CREATE DATABASE IF NOT EXISTS musicSchool')

print('Banco de dados MusicSchool criado com sucesso!')

# Fechando a conexao
cursor.close()
conexao.close()

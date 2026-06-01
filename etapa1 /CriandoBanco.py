import mysql.connector

# Tenta estabelecer a conexao e criar o banco, capturando possiveis erros
try:
    # Conecta ao servidor MySQL sem especificar um banco de dados
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password=''
    )

    # Cria o cursor responsavel por enviar e receber dados do MySQL
    cursor = conexao.cursor()

    # Executa o comando DDL para criar o banco apenas se ele nao existir
    cursor.execute('CREATE DATABASE IF NOT EXISTS musicSchool')

    print('Banco de dados MusicSchool verificado/criado com sucesso!')

except mysql.connector.Error as erro:
    # Captura e exibe falhas de conexao ou de execucao do comando
    print(f'Erro ao conectar ou criar o banco: {erro}')

finally:
    # Garante que o cursor e a conexao serao fechados liberando recursos
    if 'cursor' in locals():
        cursor.close()
    if 'conexao' in locals() and conexao.is_connected():
        conexao.close()
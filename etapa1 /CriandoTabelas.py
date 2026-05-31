
import mysql.connector

# Conectando ao MySQL
conexao = mysql.connector.connect (
    host='localhost',
    user='root',
    password='',
    database='musicSchool'
)

if conexao.is_connected():
        print('Conexão com o MySQL estabelecida com sucesso!')

        # Cria um cursor para executar comandos SQL
        cursor = conexao.cursor()

        try:
            comando_sql1 = '''
            CREATE TABLE IF NOT EXISTS alunos (
                id_aluno INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                telefone VARCHAR(20) NOT NULL,
                idade INT NULL,
                email VARCHAR(100) NULL
            )'''

            comando_sql2 = '''
            CREATE TABLE IF NOT EXISTS professores (
                id_professor INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                instrumento_principal VARCHAR(50) NOT NULL,
                anos_experiencia INT NULL,
                telefone VARCHAR(20) NULL
            )'''

            comando_sql3 = '''
            CREATE TABLE IF NOT EXISTS instrumentos (
                id_instrumento INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(50) NOT NULL,
                categoria VARCHAR(50) NOT NULL,
                marca VARCHAR(50) NULL,
                qtd_disponivel INT DEFAULT 0
            )'''

            comando_sql4 = '''
            CREATE TABLE IF NOT EXISTS matriculas (
                id_matricula INT AUTO_INCREMENT PRIMARY KEY,
                id_aluno INT NOT NULL,
                id_professor INT NOT NULL,
                id_instrumento INT NOT NULL,
                dia_semana VARCHAR(20) NOT NULL,
                horario TIME NOT NULL,
                valor_mensal DECIMAL(10,2) NOT NULL
            )'''
        

            # Executa todos os comandos de criação das tabelas
            cursor.execute(comando_sql1)
            cursor.execute(comando_sql2)
            cursor.execute(comando_sql3)
            cursor.execute(comando_sql4)

            print('Tabelas criadas com sucesso!')

            # Mostra as tabelas existentes no banco
            cursor.execute('SHOW TABLES')
            for tabela in cursor:
                print(f'Tabela encontrada: {tabela[0]}')

        except mysql.connector.Error as erro:
            # Trata erros de execução SQL
            print(f'Erro ao executar comandos SQL: {erro}')

        finally:
            # Fecha o cursor, mesmo se houver erro
            cursor.close()

else:
    # Caso a conexão não tenha sido estabelecida
    print('Não foi possível conectar ao MySQL.')
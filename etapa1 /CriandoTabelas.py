import mysql.connector

# Bloco try principal para proteger a tentativa de conexao com o banco
try:
    # Conecta diretamente ao banco de dados recem-criado
    conexao = mysql.connector.connect (
        host='localhost',
        user='root',
        password='',
        database='musicSchool'
    )

    # Verifica se o objeto de conexao esta ativo
    if conexao.is_connected():
        print('Conexao com o MySQL estabelecida com sucesso!')

        # Instancia o cursor para execucao dos scripts SQL
        cursor = conexao.cursor()

        try:
            # Comando para criar a tabela de alunos com chave primaria autoincremento
            comando_sql1 = '''
            CREATE TABLE IF NOT EXISTS alunos (
                id_aluno INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                telefone VARCHAR(20) NOT NULL,
                idade INT NULL,
                email VARCHAR(100) NULL
            )'''

            # Comando para criar a tabela de professores
            comando_sql2 = '''
            CREATE TABLE IF NOT EXISTS professores (
                id_professor INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                instrumento_principal VARCHAR(50) NOT NULL,
                anos_experiencia INT NULL,
                telefone VARCHAR(20) NULL
            )'''

            # Comando para criar a tabela de instrumentos com valor padrao de estoque
            comando_sql3 = '''
            CREATE TABLE IF NOT EXISTS instrumentos (
                id_instrumento INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(50) NOT NULL,
                categoria VARCHAR(50) NOT NULL,
                marca VARCHAR(50) NULL,
                qtd_disponivel INT DEFAULT 0
            )'''

            # Comando para criar a tabela associativa de matriculas 
            # Implementadas as restricoes de Chave Estrangeira (FOREIGN KEY) para garantir integridade referencial
            comando_sql4 = '''
            CREATE TABLE IF NOT EXISTS matriculas (
                id_matricula INT AUTO_INCREMENT PRIMARY KEY,
                id_aluno INT NOT NULL,
                id_professor INT NOT NULL,
                id_instrumento INT NOT NULL,
                dia_semana VARCHAR(20) NOT NULL,
                horario TIME NOT NULL,
                valor_mensal DECIMAL(10,2) NOT NULL,
            )'''
        
            # Executa os comandos SQL em sequencia para estruturar o banco
            cursor.execute(comando_sql1)
            cursor.execute(comando_sql2)
            cursor.execute(comando_sql3)
            cursor.execute(comando_sql4)

            print('Tabelas validadas/criadas com sucesso!')

            # Realiza uma consulta ao banco para listar as tabelas geradas
            cursor.execute('SHOW TABLES')
            
            # Itera sobre o resultado da consulta e exibe o nome de cada tabela
            for tabela in cursor:
                print(f'Tabela encontrada: {tabela[0]}')

        except mysql.connector.Error as erro:
            # Intercepta erros especificos na construcao das tabelas ou na sintaxe SQL
            print(f'Erro ao executar comandos SQL: {erro}')

        finally:
            # Encerra o cursor para evitar vazamento de memoria no banco
            if 'cursor' in locals():
                cursor.close()

except mysql.connector.Error as erro:
    # Tratamento caso o banco musicSchool nao exista ou o servidor esteja inacessivel
    print(f'Nao foi possivel conectar ao MySQL ou banco nao encontrado: {erro}')

finally:
    # Encerra a conexao com o banco de dados caso ela tenha sido aberta
    if 'conexao' in locals() and conexao.is_connected():
        conexao.close()
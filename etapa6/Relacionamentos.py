# Módulo de manutenção do banco de dados para aplicação de restrições (Foreign Keys)

import mysql.connector

try:
    # Estabelece a conexão com o banco de dados
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='musicSchool'
    )

    cursor = conexao.cursor()

    # Lista de comandos para vincular as tabelas através de chaves estrangeiras
    # As chaves garantem a integridade referencial, impedindo matrículas de alunos ou professores inexistentes
    comandos_sql = [
        '''ALTER TABLE matriculas 
           ADD CONSTRAINT fk_aluno 
           FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno)''',
           
        '''ALTER TABLE matriculas 
           ADD CONSTRAINT fk_professor 
           FOREIGN KEY (id_professor) REFERENCES professores(id_professor)''',
           
        '''ALTER TABLE matriculas 
           ADD CONSTRAINT fk_instrumento 
           FOREIGN KEY (id_instrumento) REFERENCES instrumentos(id_instrumento)'''
    ]

    # Executa cada comando de alteração individualmente
    for comando in comandos_sql:
        try:
            cursor.execute(comando)
            print('Chave estrangeira aplicada com sucesso.')
        except mysql.connector.Error as erro:
            # Captura erro caso a chave já tenha sido aplicada anteriormente
            print(f'Aviso: Não foi possível aplicar uma das chaves (pode já existir): {erro.msg}')

    # Consulta o dicionário de dados do MySQL (information_schema) para listar as chaves aplicadas
    cursor.execute('''
        SELECT CONSTRAINT_NAME 
        FROM information_schema.KEY_COLUMN_USAGE 
        WHERE TABLE_SCHEMA = 'musicSchool' 
        AND TABLE_NAME = 'matriculas' 
        AND REFERENCED_TABLE_NAME IS NOT NULL;
    ''')

    print('\nChaves Estrangeiras configuradas na tabela matriculas:')
    for fk in cursor:
        print(f'- {fk[0]}')

except mysql.connector.Error as erro:
    print(f'Erro de conexão com o banco de dados: {erro}')

finally:
    # Fecha os recursos de forma segura
    if 'cursor' in locals():
        cursor.close()
    if 'conexao' in locals() and conexao.is_connected():
        conexao.close()
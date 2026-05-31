import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='musicSchool'
)

cursor = conexao.cursor()

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

# Executando cada comando de alteração
for comando in comandos_sql:
    cursor.execute(comando)

print('Chaves estrangeiras (Foreign Keys) aplicadas com sucesso na tabela matriculas!')

# Verificando as chaves estrangeiras criadas no banco
cursor.execute('''
    SELECT CONSTRAINT_NAME 
    FROM information_schema.KEY_COLUMN_USAGE 
    WHERE TABLE_SCHEMA = 'musicSchool' 
    AND TABLE_NAME = 'matriculas' 
    AND REFERENCED_TABLE_NAME IS NOT NULL;
''')

for fk in cursor:
    print(f'Chave Estrangeira encontrada: {fk[0]}')

cursor.close()
conexao.close()
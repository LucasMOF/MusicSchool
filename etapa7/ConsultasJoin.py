# Módulo para consultas avançadas utilizando cruzamento de tabelas (JOINs)

import etapa2.RegristrarDados as e2
import etapa3.Consultas as e3

# Função para relátorio de matriculas
def listar_matriculas_detalhadas(cursor):
    print('\n=== RELATÓRIO DE MATRÍCULAS (INNER JOIN) ===')
    
    # INNER JOIN combina registros onde há correspondência nas tabelas vinculadas.
    # Se uma matrícula não tiver um aluno ou professor válido, ela não aparecerá aqui.
    comando = '''
        SELECT 
            m.id_matricula, 
            a.nome AS aluno, 
            p.nome AS professor, 
            i.nome AS instrumento,
            m.dia_semana,
            m.horario
        FROM matriculas m
        INNER JOIN alunos a ON m.id_aluno = a.id_aluno
        INNER JOIN professores p ON m.id_professor = p.id_professor
        INNER JOIN instrumentos i ON m.id_instrumento = i.id_instrumento
        ORDER BY m.id_matricula ASC
    '''
    cursor.execute(comando)
    resultados = cursor.fetchall()
    
    if not resultados:
        print("Nenhuma matrícula encontrada.")
    else:
        print(f"{'ID':<5} | {'Aluno':<20} | {'Professor':<20} | {'Instrumento':<15} | {'Dia/Hora':<20}")
        print("-" * 88)
        for linha in resultados:
            print(f"{linha[0]:<5} | {linha[1]:<20} | {linha[2]:<20} | {linha[3]:<15} | {linha[4]} às {linha[5]}")
    print("-" * 88)

# Função para listar as turmas dos professores
def listar_professores_e_turmas(cursor):
    print('\n=== CARGA HORÁRIA DOS PROFESSORES (LEFT JOIN) ===')
    
    # LEFT JOIN preserva todos os registros da tabela à esquerda (professores),
    # mesmo que não possuam correspondência na tabela de matrículas.
    comando = '''
        SELECT 
            p.id_professor, 
            p.nome, 
            COUNT(m.id_matricula) AS total_alunos
        FROM professores p
        LEFT JOIN matriculas m ON p.id_professor = m.id_professor
        GROUP BY p.id_professor, p.nome
        ORDER BY total_alunos DESC
    '''
    cursor.execute(comando)
    resultados = cursor.fetchall()
    
    if not resultados:
        print("Nenhum professor encontrado no sistema.")
    else:
        print(f"{'ID':<5} | {'Professor':<25} | {'Alunos Matriculados':<20}")
        print("-" * 56)
        for linha in resultados:
            print(f"{linha[0]:<5} | {linha[1]:<25} | {linha[2]:<20}")
    print("-" * 56)

# Função para listar os alunos que estão matriculados a um professor específico
def listar_alunos_por_professor_especifico(cursor):
    print('\n=== ALUNOS DE UM PROFESSOR ESPECÍFICO ===')
    
    # Lista professores para que o usuário possa escolher um ID válido
    e3.listar_todos_professores(cursor)
    id_prof = e2.ler_inteiro('\nInforme o ID do professor para ver sua turma: ', obrigatorio=True)
    
    # Utiliza INNER JOIN para filtrar apenas as matrículas do professor selecionado
    comando = '''
        SELECT 
            a.nome AS aluno, 
            i.nome AS instrumento,
            m.dia_semana,
            m.horario
        FROM matriculas m
        INNER JOIN alunos a ON m.id_aluno = a.id_aluno
        INNER JOIN instrumentos i ON m.id_instrumento = i.id_instrumento
        WHERE m.id_professor = %s
    '''
    cursor.execute(comando, (id_prof,))
    resultados = cursor.fetchall()
    
    if not resultados:
        print("Este professor não possui alunos matriculados no momento.")
    else:
        print(f"\n{'Aluno':<25} | {'Instrumento':<20} | {'Dia/Horário':<20}")
        print("-" * 70)
        for linha in resultados:
            print(f"{linha[0]:<25} | {linha[1]:<20} | {linha[2]} às {linha[3]}")
    print("-" * 70)

# Função para listar instrumentos que não foram escolhidos
def listar_instrumentos_nao_escolhidos(cursor):
    print('\n=== INSTRUMENTOS NUNCA ESCOLHIDOS (LEFT JOIN + IS NULL) ===')
    
    # A técnica LEFT JOIN seguida de WHERE ... IS NULL é usada para identificar 
    # registros "órfãos" ou sem relação na outra tabela.
    comando = '''
        SELECT 
            i.id_instrumento, 
            i.nome, 
            i.categoria
        FROM instrumentos i
        LEFT JOIN matriculas m ON i.id_instrumento = m.id_instrumento
        WHERE m.id_matricula IS NULL
    '''
    cursor.execute(comando)
    resultados = cursor.fetchall()
    
    if not resultados:
        print("Excelente! Todos os instrumentos do nosso catálogo possuem pelo menos um aluno matriculado.")
    else:
        print(f"{'ID':<5} | {'Instrumento':<25} | {'Categoria':<20}")
        print("-" * 55)
        for linha in resultados:
            print(f"{linha[0]:<5} | {linha[1]:<25} | {linha[2]:<20}")
    print("-" * 55)
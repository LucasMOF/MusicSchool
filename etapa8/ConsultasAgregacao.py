# etapa8/Agregacoes.py
# Módulo para cálculos e relatórios analíticos (Funções de Agregação e GROUP BY)

def calcular_receita_total(cursor):
    print('\n=== 4. RECEITA MENSAL TOTAL ===')
    
    # SUM: Soma todos os valores da coluna
    comando = "SELECT SUM(valor_mensal) FROM matriculas"
    cursor.execute(comando)
    resultado = cursor.fetchone()
    
    total = resultado[0] if resultado[0] is not None else 0.0
    
    print(f"A receita total da escola com matrículas ativas é: R$ {total:.2f}")
    print("-" * 40)

def professor_maior_receita(cursor):
    print('\n=== 6. PROFESSOR COM MAIOR RECEITA ===')
    
    # Agrupa por professor, soma as matrículas dele, ordena do maior pro menor e pega o 1º (LIMIT 1)
    comando = '''
        SELECT 
            p.nome, 
            SUM(m.valor_mensal) AS receita_gerada
        FROM professores p
        INNER JOIN matriculas m ON p.id_professor = m.id_professor
        GROUP BY p.id_professor, p.nome
        ORDER BY receita_gerada DESC
        LIMIT 1
    '''
    cursor.execute(comando)
    resultado = cursor.fetchone()
    
    if not resultado:
        print("Nenhuma matrícula registrada para calcular receita.")
    else:
        print(f"🏆 O(a) professor(a) {resultado[0]} gera a maior receita: R$ {resultado[1]:.2f}")
    print("-" * 45)

def alunos_multiplos_instrumentos(cursor):
    print('\n=== 8. ALUNOS EM MAIS DE UM INSTRUMENTO ===')
    
    # O HAVING filtra o resultado do GROUP BY (só mostra quem tem COUNT > 1)
    comando = '''
        SELECT 
            a.nome, 
            COUNT(m.id_instrumento) AS qtd_instrumentos
        FROM alunos a
        INNER JOIN matriculas m ON a.id_aluno = m.id_aluno
        GROUP BY a.id_aluno, a.nome
        HAVING qtd_instrumentos > 1
    '''
    cursor.execute(comando)
    resultados = cursor.fetchall()
    
    if not resultados:
        print("No momento, nenhum aluno cursa mais de um instrumento.")
    else:
        print(f"{'Aluno':<25} | {'Qtd. Instrumentos':<15}")
        print("-" * 45)
        for linha in resultados:
            print(f"{linha[0]:<25} | {linha[1]:<15}")
    print("-" * 45)

def matriculas_por_dia(cursor):
    print('\n=== 9. MATRÍCULAS POR DIA DA SEMANA ===')
    
    comando = '''
        SELECT 
            dia_semana, 
            COUNT(id_matricula) AS total_aulas
        FROM matriculas
        GROUP BY dia_semana
        ORDER BY total_aulas DESC
    '''
    cursor.execute(comando)
    resultados = cursor.fetchall()
    
    if not resultados:
        print("Nenhuma matrícula registrada.")
    else:
        print(f"{'Dia da Semana':<20} | {'Total de Aulas':<15}")
        print("-" * 40)
        for linha in resultados:
            print(f"{linha[0]:<20} | {linha[1]:<15}")
    print("-" * 40)
# etapa3/Consultas.py
# Módulo de consultas básicas (Listagens Gerais e Filtros Simples)

import etapa2.RegristrarDados as e2

# ==========================================
# Listagens Gerais (SELECT Geral)
# ==========================================

def listar_todos_alunos(cursor):
    print('\n--- LISTA DE TODOS OS ALUNOS ---')
    cursor.execute("SELECT id_aluno, nome, telefone, idade, email FROM alunos")
    resultados = cursor.fetchall()
    
    if not resultados:
        print("Nenhum aluno cadastrado.")
    else:
        print(f"{'ID':<5} | {'Nome':<25} | {'Telefone':<15} | {'Idade':<5} | {'Email':<20}")
        print("-" * 75)
        for alu in resultados:
            idade = alu[3] if alu[3] else "N/A"
            email = alu[4] if alu[4] else "N/A"
            print(f"{alu[0]:<5} | {alu[1]:<25} | {alu[2]:<15} | {idade:<5} | {email:<20}")
    print("-" * 75)

def listar_todos_professores(cursor):
    print('\n--- LISTA DE TODOS OS PROFESSORES ---')
    cursor.execute("SELECT id_professor, nome, instrumento_principal, anos_experiencia FROM professores")
    resultados = cursor.fetchall()
    
    if not resultados:
        print("Nenhum professor cadastrado.")
    else:
        print(f"{'ID':<5} | {'Nome':<25} | {'Instrumento Principal':<25} | {'Exp. (Anos)':<12}")
        print("-" * 73)
        for prof in resultados:
            exp = prof[3] if prof[3] is not None else "N/A"
            print(f"{prof[0]:<5} | {prof[1]:<25} | {prof[2]:<25} | {exp:<12}")
    print("-" * 73)

def listar_todos_instrumentos(cursor):
    print('\n--- LISTA DE TODOS OS INSTRUMENTOS ---')
    cursor.execute("SELECT id_instrumento, nome, categoria, marca, qtd_disponivel FROM instrumentos")
    resultados = cursor.fetchall()
    
    if not resultados:
        print("Nenhum instrumento cadastrado.")
    else:
        print(f"{'ID':<5} | {'Nome':<20} | {'Categoria':<15} | {'Marca':<15} | {'Estoque':<8}")
        print("-" * 70)
        for inst in resultados:
            marca = inst[3] if inst[3] else "N/A"
            print(f"{inst[0]:<5} | {inst[1]:<20} | {inst[2]:<15} | {marca:<15} | {inst[4]:<8}")
    print("-" * 70)


# ==========================================
# Consultas com Filtros (WHERE e ORDER BY)
# ==========================================

def listar_instrumentos_baixo_estoque(cursor):
    print('\n--- FILTRAR INSTRUMENTOS POR ESTOQUE ---')
    limite = e2.ler_inteiro('Mostrar instrumentos com quantidade abaixo de: ', obrigatorio=True)
    
    comando = "SELECT id_instrumento, nome, categoria, qtd_disponivel FROM instrumentos WHERE qtd_disponivel < %s"
    cursor.execute(comando, (limite,))
    resultados = cursor.fetchall()
    
    if not resultados:
        print(f"Nenhum instrumento com estoque menor que {limite}.")
    else:
        print(f"\n... Exibindo estoque menor que {limite} ...")
        print(f"{'ID':<5} | {'Instrumento':<20} | {'Categoria':<15} | {'Estoque':<5}")
        print("-" * 55)
        for inst in resultados:
            print(f"{inst[0]:<5} | {inst[1]:<20} | {inst[2]:<15} | {inst[3]:<5}")
    print("-" * 55)

def listar_matriculas_por_valor(cursor):
    print('\n--- FILTRAR MATRÍCULAS POR VALOR ---')
    valor_min = e2.ler_float('Mostrar matrículas com valor acima de (Ex: 100.00): ', obrigatorio=True)
    
    comando = "SELECT id_matricula, id_aluno, id_professor, valor_mensal FROM matriculas WHERE valor_mensal > %s ORDER BY valor_mensal DESC"
    cursor.execute(comando, (valor_min,))
    resultados = cursor.fetchall()
    
    if not resultados:
        print(f"Nenhuma matrícula com valor acima de R$ {valor_min:.2f}.")
    else:
        print(f"\n... Exibindo acima de R$ {valor_min:.2f} (Do mais caro ao mais barato) ...")
        print(f"{'ID Mat.':<8} | {'ID Aluno':<10} | {'ID Prof.':<10} | {'Valor Mensal':<15}")
        print("-" * 50)
        for mat in resultados:
            print(f"{mat[0]:<8} | {mat[1]:<10} | {mat[2]:<10} | R$ {mat[3]:.2f}")
    print("-" * 50)
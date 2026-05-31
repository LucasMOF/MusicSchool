# etapa4/Atualizar.py
# Módulo para atualização de registros existentes (UPDATE, SET, WHERE)

import etapa2.RegristrarDados as e2
import etapa3.Consultas as e3

def atualizar_estoque_instrumento(cursor, conexao):
    print('\n=== ATUALIZAR ESTOQUE DE INSTRUMENTO ===')
    e3.listar_todos_instrumentos(cursor)
    
    id_inst = e2.ler_inteiro('\nInforme o ID do instrumento para atualizar: ', obrigatorio=True)
    nova_qtd = e2.ler_inteiro('Nova quantidade em estoque: ', obrigatorio=True, minimo=0)

    comando = "UPDATE instrumentos SET qtd_disponivel = %s WHERE id_instrumento = %s"
    
    try:
        cursor.execute(comando, (nova_qtd, id_inst))
        conexao.commit() # O commit é essencial para gravar a alteração no banco
        
        # rowcount verifica quantas linhas foram afetadas pelo comando
        if cursor.rowcount > 0:
            print("Estoque atualizado com sucesso!")
        else:
            print("Ocorreu um problema. Verifique se o ID está correto.")
    except Exception as erro:
        print(f"Erro ao atualizar o estoque: {erro}")
        conexao.rollback()

def atualizar_valor_matricula(cursor, conexao):
    print('\n=== REAJUSTAR VALOR DA MATRÍCULA ===')
    # Listar as matrículas antes (uma consulta rápida direto aqui ou reaproveitando se houver)
    cursor.execute("SELECT id_matricula, id_aluno, valor_mensal FROM matriculas")
    matriculas = cursor.fetchall()
    
    if not matriculas:
        print("Nenhuma matrícula encontrada.")
        return
        
    print(f"\n{'ID Mat.':<8} | {'ID Aluno':<10} | {'Valor Atual':<15}")
    print("-" * 40)
    for mat in matriculas:
        print(f"{mat[0]:<8} | {mat[1]:<10} | R$ {mat[2]:.2f}")
    print("-" * 40)

    id_mat = e2.ler_inteiro('\nInforme o ID da Matrícula para reajustar: ', obrigatorio=True)
    novo_valor = e2.ler_float('Novo valor mensal (Ex: 160.00): ', obrigatorio=True, minimo=0.0)

    comando = "UPDATE matriculas SET valor_mensal = %s WHERE id_matricula = %s"
    
    try:
        cursor.execute(comando, (novo_valor, id_mat))
        conexao.commit()
        
        if cursor.rowcount > 0:
            print("Valor da matrícula atualizado com sucesso!")
        else:
            print("ID da matrícula não encontrado.")
    except Exception as erro:
        print(f"Erro ao atualizar a matrícula: {erro}")
        conexao.rollback()

def atualizar_contato_aluno(cursor, conexao):
    print('\n=== ATUALIZAR CONTATO DO ALUNO ===')
    e3.listar_todos_alunos(cursor)
    
    id_aluno = e2.ler_inteiro('\nInforme o ID do aluno: ', obrigatorio=True)
    novo_telefone = e2.ler_texto('Novo Telefone: ', obrigatorio=True)
    novo_email = e2.ler_texto('Novo Email: ', obrigatorio=True)

    comando = "UPDATE alunos SET telefone = %s, email = %s WHERE id_aluno = %s"
    
    try:
        cursor.execute(comando, (novo_telefone, novo_email, id_aluno))
        conexao.commit()
        
        if cursor.rowcount > 0:
            print("Contato do aluno atualizado com sucesso!")
        else:
            print("ID do aluno não encontrado.")
    except Exception as erro:
        print(f"rro ao atualizar contato: {erro}")
        conexao.rollback()
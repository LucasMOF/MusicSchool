# etapa5/Remover.py
# Módulo para remoção de registros (DELETE, WHERE e Confirmação)

import etapa2.RegristrarDados as e2
import etapa3.Consultas as e3

def cancelar_matricula(cursor, conexao):
    print('\n=== CANCELAR MATRÍCULA ===')
    
    # Exibe as matrículas existentes para o usuário ver os IDs
    cursor.execute("SELECT id_matricula, id_aluno, valor_mensal FROM matriculas")
    matriculas = cursor.fetchall()
    
    if not matriculas:
        print("Nenhuma matrícula ativa encontrada no sistema.")
        return
        
    print(f"\n{'ID Mat.':<8} | {'ID Aluno':<10} | {'Valor Mensal':<15}")
    print("-" * 40)
    for mat in matriculas:
        print(f"{mat[0]:<8} | {mat[1]:<10} | R$ {mat[2]:.2f}")
    print("-" * 40)

    id_mat = e2.ler_inteiro('\nInforme o ID da Matrícula que deseja cancelar: ', obrigatorio=True)

    # Mecanismo de Confirmação antes da Exclusão
    confirmacao = e2.ler_texto(f'⚠️ Tem certeza que deseja excluir a matrícula ID {id_mat}? (S/N): ', obrigatorio=True)
    
    if confirmacao.upper() == 'S':
        comando = "DELETE FROM matriculas WHERE id_matricula = %s"
        try:
            cursor.execute(comando, (id_mat,))
            conexao.commit()
            
            if cursor.rowcount > 0:
                print("Matrícula cancelada e removida com sucesso!")
            else:
                print("ID da matrícula não foi encontrado.")
        except Exception as erro:
            print(f"Erro ao remover a matrícula: {erro}")
            conexao.rollback()
    else:
        print("Operação cancelada pelo usuário. A matrícula não foi alterada.")

def remover_aluno(cursor, conexao):
    print('\n=== REMOVER CADASTRO DE ALUNO ===')
    e3.listar_todos_alunos(cursor)
    
    id_aluno = e2.ler_inteiro('\nInforme o ID do aluno que deseja remover: ', obrigatorio=True)
    
    confirmacao = e2.ler_texto(f'⚠️ Tem certeza que deseja remover o aluno ID {id_aluno}? (S/N): ', obrigatorio=True)
    
    if confirmacao.upper() == 'S':
        comando = "DELETE FROM alunos WHERE id_aluno = %s"
        try:
            cursor.execute(comando, (id_aluno,))
            conexao.commit()
            
            if cursor.rowcount > 0:
                print("Aluno removido com sucesso!")
            else:
                print("ID do aluno não foi encontrado.")
                
        except Exception as erro:
            # Captura o erro caso o aluno tenha matrículas vinculadas (Foreign Key Constraint)
            print(f"\nNão foi possível remover o aluno.")
            print(f"Motivo: O aluno possui matrículas ativas vinculadas a ele. Cancele as matrículas antes.")
            conexao.rollback()
    else:
        print("Operação cancelada. O aluno não foi removido.")
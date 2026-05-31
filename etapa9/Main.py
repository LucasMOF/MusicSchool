# Modulo principal: responsavel por orquestrar o menu, a conexao e o fluxo do sistema

import sys
import os

# Ajusta o caminho do Python para permitir a importacao entre pastas do projeto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mysql.connector

# Importacao de todos os modulos funcionais do sistema
import etapa2.RegristrarDados as e2
import etapa3.Consultas as e3
import etapa4.Update as e4
import etapa5.Delete as e5  
import etapa7.ConsultasJoin as e7
import etapa8.ConsultasAgregacao as e8

def iniciar_sistema():
    try:
        # Estabelece a conexao inicial com o banco de dados 'musicSchool'
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='musicSchool',
        )

        if conexao.is_connected():
            print('Conexao com o banco de dados estabelecida!')
            # O cursor e criado uma unica vez e passado como referencia para as funcoes
            cursor = conexao.cursor()
            
            def menu():
                # Exibicao do menu principal dividido por responsabilidades
                print('\n==================================================')
                print('              SISTEMA MUSIC SCHOOL                ')
                print('==================================================')
                
                print('\n--- CADASTROS ---')
                print('  1 - Cadastrar Aluno')
                print('  2 - Cadastrar Professor')
                print('  3 - Cadastrar Instrumento')
                print('  4 - Efetuar Matricula') 
                
                print('\n--- LISTAGENS BASICAS ---')
                print('  5 - Listar Todos os Alunos')
                print('  6 - Listar Todos os Professores')
                print('  7 - Listar Todos os Instrumentos')
                
                print('\n--- BUSCAS AVANCADAS ---')
                print('  8 - Buscar Instrumentos com Baixo Estoque')
                print('  9 - Buscar Matriculas por Valor Minimo')

                print('\n--- LISTAGENS AVANCADAS ---')
                print(' 10 - Alunos em Multiplos Instrumentos')
                print(' 11 - Matriculas por Dia da Semana')
                print(' 12 - Ver Turma de um Professor')
                print(' 13 - Instrumentos Nunca Escolhidos')   
                
                print('\n--- ATUALIZACOES (UPDATE) ---')
                print(' 14 - Atualizar Estoque de Instrumento')
                print(' 15 - Reajustar Valor de Matricula')
                print(' 16 - Atualizar Contato de Aluno')
                
                print('\n--- REMOCOES (DELETE) ---')
                print(' 17 - Cancelar Matricula')
                print(' 18 - Remover Aluno') 
                
                print('\n--- RELATORIOS E ESTATISTICAS ---')
                print(' 19 - Relatorio de Matriculas')
                print(' 20 - Carga Horaria dos Professores')
                print(' 21 - Calcular Receita Mensal Total')
                print(' 22 - Professor com Maior Receita')
                
                print('\n--------------------------------------------------')
                print('  0 - Sair do Sistema')
                print('==================================================\n')

            # Loop principal de controle do sistema
            while True:
                menu()
                # Leitura da opcao do usuario utilizando a funcao de validacao da etapa 2
                opcao = e2.ler_texto('Escolha uma opcao: ', obrigatorio=True)

                # Estrutura match-case para delegar a execucao para o modulo/funcao correspondente
                match opcao:
                    case '1': e2.cadastrar_aluno(cursor, conexao)
                    case '2': e2.cadastrar_professor(cursor, conexao)
                    case '3': e2.cadastrar_instrumento(cursor, conexao)
                    case '4': e2.cadastrar_matricula(cursor, conexao)
                    case '5': e3.listar_todos_alunos(cursor)
                    case '6': e3.listar_todos_professores(cursor)
                    case '7': e3.listar_todos_instrumentos(cursor)
                    case '8': e3.listar_instrumentos_baixo_estoque(cursor)
                    case '9': e3.listar_matriculas_por_valor(cursor)
                    case '10': e8.alunos_multiplos_instrumentos(cursor)
                    case '11': e8.matriculas_por_dia(cursor)
                    case '12': e7.listar_alunos_por_professor_especifico(cursor)
                    case '13': e7.listar_instrumentos_nao_escolhidos(cursor)
                    case '14': e4.atualizar_estoque_instrumento(cursor, conexao)
                    case '15': e4.atualizar_valor_matricula(cursor, conexao)
                    case '16': e4.atualizar_contato_aluno(cursor, conexao)
                    case '17': e5.cancelar_matricula(cursor, conexao)
                    case '18': e5.remover_aluno(cursor, conexao)
                    case '19': e7.listar_matriculas_detalhadas(cursor)
                    case '20': e7.listar_professores_e_turmas(cursor)
                    case '21': e8.calcular_receita_total(cursor)
                    case '22': e8.professor_maior_receita(cursor)
                    case '0':
                        print('Encerrando o sistema...')
                        break
                    case _:
                        print('Opção inválida. Escolha um número de 0 a 22.\n')

        else:
            print('Não foi possível estabelecer conexão com o banco de dados.')

    except mysql.connector.Error as erro:
        # Tratamento de erro global para problemas de conexão ou falta do banco
        print(f'Erro ao conectar ao MySQL: {erro}')

    finally:
        # Garante o fechamento dos recursos do banco, evitando consumo desnecessario de memória
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conexao' in locals() and conexao.is_connected():
            conexao.close()

# Ponto de entrada do script
if __name__ == "__main__":
    iniciar_sistema()
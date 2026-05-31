# Módulo contendo as funções de validação de entrada e inserção de dados no banco (CREATE)

import mysql.connector

# ==========================================
# Funções Auxiliares de Validação de Input
# ==========================================

def ler_texto(mensagem, obrigatorio=True):
    # Loop infinito que só quebra quando o usuário digitar um texto válido
    while True:
        # strip() remove espaços em branco acidentais no início e fim da string
        valor = input(mensagem).strip()
        
        # Verifica se a string ficou vazia após a limpeza
        if valor == "":
            if obrigatorio:
                print("Erro: Este campo é obrigatório e não pode ficar em branco.\n")
                continue 
            else:
                # Retorna None (nulo) para o banco de dados se o campo for opcional
                return None 
                
        return valor

def ler_inteiro(mensagem, obrigatorio=False, minimo=None):
    # Função que garante a digitação de um número inteiro válido
    while True:
        entrada = input(mensagem).strip()
        if not entrada:
            if obrigatorio:
                print('Este campo é obrigatório.')
                continue
            return None
        
        # Tenta converter a string digitada para um número inteiro (int)
        try:
            valor = int(entrada)
            # Verifica se o número digitado é menor que o limite mínimo permitido
            if minimo is not None and valor < minimo:
                print(f'Valor inválido. O número não pode ser menor que {minimo}.')
                continue
            return valor
        except ValueError:
            # Captura o erro caso o usuário digite letras ou números decimais
            print('Erro: Digite apenas números inteiros válidos (sem letras ou pontos).')

def ler_float(mensagem, obrigatorio=False, minimo=None):
    # Função que garante a digitação de valores decimais (como moeda)
    while True:
        # replace() converte vírgula brasileira em ponto americano para o Python aceitar a conversão
        entrada = input(mensagem).strip().replace(',', '.')
        if not entrada:
            if obrigatorio:
                print('Este campo é obrigatório.')
                continue
            return None
            
        try:
            valor = float(entrada)
            if minimo is not None and valor < minimo:
                print(f'Valor inválido. O número não pode ser menor que {minimo}.')
                continue
            return valor
        except ValueError:
            print('Erro: Digite um número decimal válido (ex: 150.00).')

def validar_id_existe(cursor, tabela, coluna_id, id_informado):
    # Verifica no banco de dados se o ID fornecido existe na tabela alvo
    comando = f"SELECT {coluna_id} FROM {tabela} WHERE {coluna_id} = %s"
    cursor.execute(comando, (id_informado,))
    resultado = cursor.fetchone()
    return resultado is not None

# ==========================================
# Função Global de Execução no Banco
# ==========================================

def executar_insercao(cursor, conexao, descricao, comando_sql, dados):
    # Centraliza a lógica de salvar dados para evitar repetição de código
    try:
        # O cursor substitui os '%s' do comando_sql pela tupla 'dados' de forma segura
        cursor.execute(comando_sql, dados)
        
        # Efetiva a transação, salvando as alterações fisicamente no banco
        conexao.commit()
        print(f'{descricao} cadastrado(a) com sucesso!')
        
        # lastrowid retorna o ID (Primary Key) gerado automaticamente pelo AUTO_INCREMENT
        print(f'ID gerado: {cursor.lastrowid}\n')
        return True
        
    except mysql.connector.Error as erro:
        # Em caso de falha (ex: erro de integridade), desfaz a operação incompleta
        conexao.rollback()
        print(f'Erro do Banco de Dados ao cadastrar {descricao}: {erro}\n')
        return False

# ==========================================
# Funções Específicas de Cadastro (CREATE)
# ==========================================

def cadastrar_aluno(cursor, conexao):
    print('\n=== CADASTRO DE ALUNO ===')
    nome = ler_texto('Informe o nome do aluno: ', obrigatorio=True)
    telefone = ler_texto('Informe o telefone do aluno: ', obrigatorio=True)
    idade = ler_inteiro('Informe a idade do aluno (Enter para pular): ', obrigatorio=False, minimo=1)
    email = ler_texto('Informe o email do aluno (Enter para pular): ', obrigatorio=False)

    comando_aluno = '''
    INSERT INTO alunos (nome, telefone, idade, email)
    VALUES (%s, %s, %s, %s)'''

    dados_aluno = (nome, telefone, idade, email)
    executar_insercao(cursor, conexao, 'Aluno', comando_aluno, dados_aluno)

def cadastrar_professor(cursor, conexao):
    print('\n=== CADASTRO DE PROFESSOR ===')
    nome = ler_texto('Informe o nome do professor: ', obrigatorio=True)
    instrumento = ler_texto('Informe o instrumento principal: ', obrigatorio=True)
    anos_exp = ler_inteiro('Informe os anos de experiência (Enter para pular): ', obrigatorio=False, minimo=0)
    telefone = ler_texto('Informe o telefone do professor (Enter para pular): ', obrigatorio=False)

    comando_prof = '''
    INSERT INTO professores (nome, instrumento_principal, anos_experiencia, telefone)
    VALUES (%s, %s, %s, %s)'''

    dados_prof = (nome, instrumento, anos_exp, telefone)
    executar_insercao(cursor, conexao, 'Professor', comando_prof, dados_prof)

def cadastrar_instrumento(cursor, conexao):
    print('\n=== CADASTRO DE INSTRUMENTO ===')
    nome = ler_texto('Informe o nome do instrumento: ', obrigatorio=True)
    categoria = ler_texto('Informe a categoria (Cordas, Teclas, Sopro): ', obrigatorio=True)
    marca = ler_texto('Informe a marca (Enter para pular): ', obrigatorio=False)
    qtd = ler_inteiro('Informe a quantidade em estoque: ', obrigatorio=True, minimo=0)

    comando_inst = '''
    INSERT INTO instrumentos (nome, categoria, marca, qtd_disponivel)
    VALUES (%s, %s, %s, %s)'''

    dados_inst = (nome, categoria, marca, qtd)
    executar_insercao(cursor, conexao, 'Instrumento', comando_inst, dados_inst)

def cadastrar_matricula(cursor, conexao):
    print('\n=== EFETUAR MATRÍCULA ===')
    
    import etapa3.Consultas as e3
    
    # Validação rigorosa dos IDs informados antes de prosseguir com a inserção
    
    e3.listar_todos_alunos(cursor)
    while True:
        id_aluno = ler_inteiro('\nInforme o ID do aluno acima: ', obrigatorio=True)
        if validar_id_existe(cursor, 'alunos', 'id_aluno', id_aluno):
            break
        print("Erro: ID de aluno não encontrado. Tente novamente.")
    
    e3.listar_todos_professores(cursor)
    while True:
        id_prof = ler_inteiro('\nInforme o ID do professor acima: ', obrigatorio=True)
        if validar_id_existe(cursor, 'professores', 'id_professor', id_prof):
            break
        print("Erro: ID de professor não encontrado. Tente novamente.")
    
    e3.listar_todos_instrumentos(cursor)
    while True:
        id_inst = ler_inteiro('\nInforme o ID do instrumento acima: ', obrigatorio=True)
        if validar_id_existe(cursor, 'instrumentos', 'id_instrumento', id_inst):
            break
        print("Erro: ID de instrumento não encontrado. Tente novamente.")
    
    print('\n--- Dados da Aula ---')
    dia = ler_texto('Informe o dia da semana (Ex: Segunda-feira): ', obrigatorio=True)
    horario = ler_texto('Informe o horário da aula (HH:MM): ', obrigatorio=True)
    valor = ler_float('Informe o valor mensal (Ex: 150.00): ', obrigatorio=True, minimo=0.0)

    comando_mat = '''
    INSERT INTO matriculas (id_aluno, id_professor, id_instrumento, dia_semana, horario, valor_mensal)
    VALUES (%s, %s, %s, %s, %s, %s)'''

    dados_mat = (id_aluno, id_prof, id_inst, dia, horario, valor)
    executar_insercao(cursor, conexao, 'Matrícula', comando_mat, dados_mat)
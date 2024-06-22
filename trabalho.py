import hashlib
import os
def menuProf():
    print('1- Editar diciplina') #adicionar outro sub menu dps com editar codigo, nome, ano, turmas
    print('2- Editar avaliações')
    print('3- Editar aluno')
    print('4- logout')

def login(path = str(os.getcwd())):
    os.chdir(f'{path}/Trabalho/login')
    try:
        arquivoLogin = open('login.txt', 'r+')
        leitura = arquivoLogin.read()
        print('Digite: \n 1- Fazer login \n 2- Criar nova conta')
        resposta = input('Digite:')
        if resposta == '1':
            contaExiste = False #auxiliar para verificar se existe uma conta com o nome digitado
            while contaExiste == False:
                nome = input('digite o nome da conta: ').upper()
                for linha in leitura.split('\n'):
                    if nome == linha.split(',')[0]:
                        if nome == linha.split(',')[0]:
                            senha = input('Digite a senha: ')
                            if hashlib.sha256(senha.encode()).hexdigest() == linha.split(',')[1]: #verifica-se se a senha está correta
                                #aqui ele está logado
                                print('Você esta logado!')
                                contaExiste = True
                                mainProf(nome, path)
                                #depois que o professor terminar o arquivo vai fechar
                                arquivoLogin.close()
                            else:
                                print('senha incorreta.')
                                #senha incorreta, vai pedir nome e senha novamente
                                break
                    else:
                        print('Conta não encontrada.')
                        sair = ''
                        sair = input('Deseja sair? s/n: ')
                        if sair == 's':
                            arquivoLogin.close()
                            contaExiste = True #para acabar com o loop
                            login()
                        else:
                            break
                        #uma conta com esse nome não foi encontrada, irá pedir novamente o nome da conta ou o usuário ira para a tela inicial
                        
                
        if resposta == '2':
            tipoDeConta = input('Deseja criar conta para (1)professor ou (2)aluno: ')
            if tipoDeConta == '1' or tipoDeConta == '2':
                nome = input('digite o nome desejado para a nova conta').upper()
                for linha in leitura.split('\n'): #verifica se já existe uma conta com o mesmo nome
                        if nome == linha.split(',')[0]:
                            print('Esse nome já está sendo usado faça login:')
                            arquivoLogin.close()
                            login()
                else:
                    arquivoLogin.write(nome.upper()+',')
                    criouSenha = False #auxiliar para verificar se as senhas são iguais, caso não entra em um looping pedindo para digitar a senha
                    while criouSenha == False:
                        senha = input('Digite sua senha:')
                        confirmarSenha = input('Confirmar senha: ')
                        if senha == confirmarSenha:
                            criouSenha = True
                            if tipoDeConta == '1':
                                arquivoLogin.write(hashlib.sha256(senha.encode()).hexdigest() + ',admin'+'\n')
                            elif tipoDeConta == '2':
                                arquivoLogin.write(hashlib.sha256(senha.encode()).hexdigest() + '\n')
                            #Aqui escrevemos a senha de maneira "criptografada" e indicamos que é uma conta de professor com admin
                            print('Sua conta foi criada com sucesso!')
                            arquivoLogin.close()
                            login()
                        else:
                            criouSenha = False
                            print('A senha não é a mesma digitada anteriormente digite novemente.')
            else:
                print('A opção não exite.')
                arquivoLogin.close()
                login()
        else:
            login()
    except FileNotFoundError:
        criarArquivo = open('login.txt', 'w')
        criarArquivo.close()
        login()
        


def menuDiciplina(nomeProfessor):
    criarDiciplina = 'n'
    print('1- Criar diciplina')
    print('2- editar diciplinas')
    print('3- Criar turmas')
    print('4- editar turmas')
    resposta = input('Digite o número da ação desejada: ')
    if resposta == '1':
        CriarDiciplinas(nomeProfessor)
    if resposta == '2':
        editarDiciplinas(nomeProfessor, [])
        

def CriarDiciplinas(nomeProfessor):
    auxCriarDiciplina = 'n'
    while auxCriarDiciplina == 'n':
            nomeDiciplina = input('Digite o nome da diciplina que deseja criar')
            try:
                arquivoDiciplinas = open(f'diciplinas{nomeProfessor}.txt', 'r+')
            except FileNotFoundError:
                arquivoDiciplinas = open(f'diciplinas{nomeProfessor}.txt', 'w')
                arquivoDiciplinas.close()
                arquivoDiciplinas = open(f'diciplinas{nomeProfessor}.txt', 'r+')
            leitura = arquivoDiciplinas.read()
            if nomeDiciplina in leitura:
                for linha in leitura.split('\n'):
                    #for nome in linha.split(','):
                    if nomeDiciplina == linha.split(',')[0]:
                        auxCriarDiciplina = input('Diciplina ja existente deseja voltar? s/n: ')
                        if auxCriarDiciplina != 's':
                            break
            else:
                print('Você deve adicionar um código e indicar o ano e o semestre em que esta diciplina está sendo cursada')
                codigoDiciplina = input('Digite o código da diciplina')
                while True:
                    anoDiciplina = input('Digite o ano em que a diciplina está sendo cursada')
                    semestreDiciplina = input('Digite o semestre em que a diciplina esta sendo cursada')
                    try:
                        int(anoDiciplina)#só conferir se é um valor inteiro
                        int(semestreDiciplina)
                        str(anoDiciplina)
                        str(semestreDiciplina)
                        break
                    except ValueError:
                        print('O valor do ano e do semestre deve ser um número inteiro digite novamente')
                arquivoDiciplinas.write(nomeDiciplina + ',' + codigoDiciplina + ',' + anoDiciplina + ',' + semestreDiciplina + '\n')
                print('Diciplina criada com sucesso')
                auxCriarDiciplina = input('Deseja sair? s/n')
    arquivoDiciplinas.close()                                             

def editarDiciplinas(nomeProfessor, listasEdicoes = []):
    if input('Deseja listar suas diciplinas? s/n ') == 's':
        print(listarDiciplinas(nomeProfessor))
    nomeDiciplina = input('Digite o nome da diciplina que deseja editar: ')
    diciplinaExiste = False #variavel auxiliar para o for 
    DadosDiciplina = ''
    try:
        arquivo = open(f'diciplinas{nomeProfessor}.txt','r')
        leitura = arquivo.read()
        for linha in leitura.split('\n'):
            if nomeDiciplina == linha.split(',')[0]:
                diciplinaExiste = True
                #indicar as próximas variaveis será importante mais apra a frente para reescrever as linhas de codigo
                novoCodigo = linha.split(',')[1]
                novoAno = linha.split(',')[2]
                novoSemestre = linha.split(',')[3]
                DadosDiciplina = f'Nome: {nomeDiciplina} \nCódigo: {novoCodigo} \nAno:{novoAno} \nSemestre: {novoSemestre}'
        arquivo.close()
        if diciplinaExiste ==True:
            while True:
                print(f'Nome: {nomeDiciplina} \nCódigo: {novoCodigo} \nAno:{novoAno} \nSemestre: {novoSemestre}')
                print('1-Editar código \n2-Editar ano \n3-Editar período \n4-apagar diciplina \n5-Sair')
                resposta = input('Digite o número desejado: ')
                if resposta == '1':
                    novoCodigo = input('Digite o novo código desejado: ')
                if resposta == '2':
                    novoAno = input('Digite o novo ano desejado: ')
                if resposta == '3':
                    novoSemestre = input('Digite o novo semestre desejado: ')
                if resposta == '4':
                    apagarDiciplina(nomeProfessor, nomeDiciplina)
                    break
                if resposta == '5':
                    novaLinha = [f'{nomeDiciplina},{novoCodigo},{novoAno},{novoSemestre}']
                    listasEdicoes += novaLinha
                    break
    except FileNotFoundError:
        with open(f'diciplinas{nomeProfessor}.txt', 'w'):
            print('Você não possui nenhuma diciplina cadastrada.')
            print('Voltando para o menu.')
            return
    if diciplinaExiste == False:
        print('Diciplina não encontrada')
    if input('Deseja editar outra diciplina? s/n ') != 'n':
        
        editarDiciplinas(nomeProfessor, listasEdicoes)
    else:
        #adicionar as edições
        print(listasEdicoes) #tirar depois
        arquivo = open(f'diciplinas{nomeProfessor}.txt', 'r')
        leitura = arquivo.read()
        novoArquivo = ''
        nomesEdicoes = []
        for nomes in listasEdicoes:
            nomesEdicoes += [nomes.split(',')[0]]

        for linhas in listasEdicoes:
            print(linhas) #tirar depois
            for linha in leitura.split('\n'):
                if linhas.split(',')[0] == linha.split(',')[0]:
                    novoArquivo = novoArquivo
                else:
                    if linha.split(',')[0] not in novoArquivo and linha.split(',')[0] not in nomesEdicoes:
                        novoArquivo += f'{linha}\n'
            novoArquivo += f'{linhas}\n'
        
        
        arquivo.close()
        arquivo = open(f'diciplinas{nomeProfessor}.txt', 'w')
        arquivo.write(novoArquivo)
        print('arquivo editado com sucesso!')
        return

def apagarDiciplina(nomeProfessor, nomeDiciplina):
    arquivo = open(f'diciplinas{nomeProfessor}.txt', 'r')
    leitura = arquivo.read()
    novoArquivo = ''
    for linha in leitura.split('\n'):
        if nomeDiciplina == linha.split(',')[0]:
            novoArquivo = novoArquivo
        else:
            novoArquivo += f'{linha}\n'
    arquivo.close()
    arquivo = open(f'diciplinas{nomeProfessor}.txt', 'w')
    arquivo.write(novoArquivo)
    print('arquivo editado com sucesso!')
    return
    
def listarDiciplinas(nomeProfessor):
    try:
        arquivo = open(f'diciplinas{nomeProfessor}.txt','r')
        leitura = arquivo.read()
        diciplinas = ''
        for linha in leitura.split('\n'):
            if f'{linha.split(',')[0]}' == '':
                pass
            else:
                diciplinas += f'{linha.split(',')[0]}, '
        arquivo.close()
        return diciplinas                   
    except FileNotFoundError:
        open(f'diciplinas{nomeProfessor}.txt', 'w')
    


def mainProf(professor, path):
    os.chdir(f'{path}/Trabalho/diciplinas')
    #caso possua a caracteristica de admin ele é considerado professor
    print(f'Bem vindo {professor}')
    while True:
        menuProf()
        resposta = input('Digite o número desejado')
        if resposta == '1':
            menuDiciplina(professor)
            pass
        if resposta == '4':
            login()

def caminhoPastas():
    path = str(os.getcwd())
    try:
        
        os.makedirs(f'{path}/Trabalho')
        os.makedirs(f'{path}/Trabalho/login')
        os.makedirs(f'{path}/Trabalho/diciplinas')
    except FileExistsError:
        pass
    return path

def Start():
    path = caminhoPastas()
    login(path)

Start()
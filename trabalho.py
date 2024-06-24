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
                                print('passou por aqui')
                                arquivoLogin.close()
                            else:
                                print('senha incorreta.')
                                #senha incorreta, vai pedir nome e senha novamente
                                break
                if contaExiste ==False:
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
        


def menuDiciplina(nomeProfessor, nomeDasdiciplinas, DadosDasDiciplinas, DadosDasTurmas, NomeDasTurmas, path):
    while True:
        print(DadosDasDiciplinas) #apagar depois
        print(DadosDasTurmas)#apagar depois
        criarDiciplina = 'n'
        print('1- Criar diciplina')
        print('2- editar diciplinas')
        print('3- Criar turmas')
        print('4- editar turmas')
        print('5- salvar e sair')
        resposta = input('Digite o número da ação desejada: ')
        if resposta == '1':
            nomeDasdiciplinas, DadosDasDiciplinas = CriarDiciplinas(nomeProfessor, nomeDasdiciplinas, DadosDasDiciplinas)
        if resposta == '2':
            nomeDasdiciplinas, DadosDasDiciplinas = editarDiciplinas(nomeProfessor, nomeDasdiciplinas, DadosDasDiciplinas, [])
        if resposta == '3':
            NomeDasTurmas, DadosDasTurmas = CriarTurmas(nomeProfessor, nomeDasdiciplinas, DadosDasTurmas, NomeDasTurmas)
        if resposta == '4':
            NomeDasTurmas, DadosDasTurmas = EditarTurmas(nomeProfessor, DadosDasTurmas, NomeDasTurmas, [])
        if resposta == '5':
            salvarArquivosDiciplinas(nomeProfessor, DadosDasDiciplinas,path)
            salvarArquivosTurmas(nomeProfessor, DadosDasTurmas, path)
            break


def salvarArquivosDiciplinas(nomeProfessor, DadosDasDiciplinas,path):
    os.chdir(f'{path}/Trabalho/diciplinas')
    arquivo = open(f'diciplinas{nomeProfessor}.txt', 'w')
    for linha in DadosDasDiciplinas:
        if linha != '':
            arquivo.write(linha + '\n')
    arquivo.close() 


def salvarArquivosTurmas(nomeProfessor, DadosDasTurmas, path):
    os.chdir(f'{path}/Trabalho/turmas')
    arquivo = open('turma.txt', 'w')
    for linha in DadosDasTurmas:
        if linha != '':
            arquivo.write(linha + '\n')
    arquivo.close()


def CriarTurmas(nomeProfessor, nomeDasdiciplinas,DadosDasTurmas, NomeDasTurmas):
    while True:
        diciplina = input('Digite o nome da diciplina: ')
        if diciplina in nomeDasdiciplinas:
            nomeTurma = input('Digite o nome da turma que deseja criar: ')
            if nomeTurma in DadosDasTurmas:
                print('Turma já existe')
                if input('deseja sair? s/n') != 'n':
                    break
            else:
                codigoTurma = input('Digite o codigo da Turma: ')
                while True:
                    horarioTurma = input('Digite o horario que a turma será oferecida no estilo HH:MM: ')
                    if verificarHora(horarioTurma) == True:
                        break
                while True:
                    formaAvaliacaoTurma = input('Digite o método de avaliação, digite no estilo p1+p2+p3...pn: ')
                    if verificarMetodoAvaliacao(formaAvaliacaoTurma) == True:
                        break
                DadosDasTurmas += (nomeProfessor+ ',' + diciplina + ',' + nomeTurma + ',' + codigoTurma + ',' + horarioTurma + ',' + formaAvaliacaoTurma,)
                NomeDasTurmas += (nomeTurma,)
                if input('Deseja criar outra turma? s/n ') != 'n':
                    pass
                else:
                    break
        else:
            print('Diciplina não encontrada!')
            if input('deseja sair? s/n') != 'n':
                break
    return DadosDasTurmas

def verificarHora(horario):
    try: 
        Hora = False
        Minuto = False
        if int(horario.split(':')[0]) >= 0 and int(horario.split(':')[0]) <= 24:
            Hora = True
        if int(horario.split(':')[1]) >= 0 and int(horario.split(':')[1]) <= 60:
            Minuto = True
        if Hora ==True and Minuto == True:
            return True
        else:
            print('O valor inserido está no formato incorreto')
            return False
    except ValueError:
        print('O valor inserido está no formato incorreto')
        return False

def verificarMetodoAvaliacao(formaAvaliacaoTurma):
    try: 
        PCorreto = False
        NCorreto = False
        for avaliacoes in formaAvaliacaoTurma.split('+'):
            if len(avaliacoes) == 2:
                if avaliacoes[0] == 'p':
                    PCorreto = True
                else: 
                    print('erro p')
                    return False
                try:
                    if type(int(avaliacoes[1])) == int:
                        NCorreto = True
                    else:
                        print('erro numero')
                        return False
                except ValueError:
                    return False    
            else:
                print('erro len')
                return False
        return True

    except ValueError:
        print('Digite no formato desejado p1+p2+p3...+pn')
        return False
    
def EditarTurmas(nomeProfessor, DadosDasTurmas, NomeDasTurmas, listasEdicoes = []):
    while True:
        TurmaExiste = False
        print(DadosDasTurmas)
        nomeTurma = input('Digite o nome da turma que você deseja editar: ')
        if nomeTurma in NomeDasTurmas:
            TurmaExiste = True
            for nome in DadosDasTurmas:
                if nome.split(',')[2] == nomeTurma:
                    novaDiciplina = nome.split(',')[1]
                    novoCodigo = nome.split(',')[3]
                    novoHorario = nome.split(',')[4]
                    novaAvaliacoes = nome.split(',')[5]
        if TurmaExiste == True:
            while True:  
                print(f'Nome: {nomeTurma}\nCódigo: {novoCodigo}\nHorário:{novoHorario}\nModelo Avaliativo:{novaAvaliacoes}')        
                print('Digite o número de acordo com o que você deseja editar: \n1-Código \n2-Horario \n3-Avaliações')
                resposta = input('Digite o número desejado: ')
                if resposta == '1':
                    novoCodigo = input('Digite o novo código desejado: ')
                if resposta == '2':
                    while True:
                        novoHorario = input('Digite o novo horário no modelo HH:MM : ')
                        if verificarHora(novoHorario) == True:
                            break
                        else:
                            print('Modelo escrito errado!')
                if resposta == '3':
                    while True:
                        novaAvaliacoes = input('Digite o novo modelo de avaliações no modelo p1+p2+p3...pn: ')
                        if verificarMetodoAvaliacao == True:
                            break
                        else:
                            print('Modelo escrito errado!')
                if resposta == '4':
                    #apagar turma()
                    pass
                if resposta == '5':
                    novaLinha = [f'{nomeProfessor},{novaDiciplina},{nomeTurma},{novoCodigo},{novoHorario},{novaAvaliacoes}']
                    listasEdicoes += novaLinha
                    break
        if TurmaExiste == False:
            print('Turma não encontrada!')
        #adicionando as edições:
        novoArquivo = ()
        nomesEdicoes = []
        novoNomesDasTurmas = ()
        if listasEdicoes != []:
            for nomes in listasEdicoes:
                nomesEdicoes += [nomes.split(',')[2]]
            for nome in NomeDasTurmas:
                if NomeDasTurmas == nomeTurma:
                    pass
                else:
                    novoNomesDasTurmas += (nome,)
            for linhas in listasEdicoes:
                for linha in DadosDasTurmas:
                    if linhas.split(',')[2] == linha.split(',')[2]: #confere se os nomes são iguais
                        pass
                    else:
                        if linha not in novoArquivo and linha.split(',')[2] not in nomesEdicoes and linha != '':
                            novoArquivo += (linha,)
                novoArquivo += (linhas,)
            NomeDasTurmas = novoNomesDasTurmas
            DadosDasTurmas = novoArquivo
            print('Arquivo foi editado')
            print(NomeDasTurmas)
            print(DadosDasTurmas)
        if input('Deseja editar outra turma? s/n ') != 'n':
            pass
        else:
            break
    return NomeDasTurmas, DadosDasTurmas   

def CriarDiciplinas(nomeProfessor, nomeDasdiciplinas, DadosDasDiciplinas):
    auxCriarDiciplina = 'n'
    while auxCriarDiciplina == 'n':
            nomeDiciplina = input('Digite o nome da diciplina que deseja criar')
            if nomeDiciplina in nomeDasdiciplinas:
                auxCriarDiciplina = input('Diciplina ja existente deseja voltar? s/n: ')
                if auxCriarDiciplina != 's':
                    break
            else:
                print('Você deve adicionar um código e indicar o ano e o semestre em que esta diciplina está sendo cursada')
                codigoDiciplina = input('Digite o código da diciplina: ')
                while True:
                    anoDiciplina = input('Digite o ano em que a diciplina está sendo cursada: ')
                    semestreDiciplina = input('Digite o semestre em que a diciplina esta sendo cursada: ')
                    try:
                        int(anoDiciplina)#só conferir se é um valor inteiro
                        int(semestreDiciplina)
                        str(anoDiciplina)
                        str(semestreDiciplina)
                        break
                    except ValueError:
                        print('O valor do ano e do semestre deve ser um número inteiro digite novamente')
                while True:
                    horariosDiciplinas = input('Digite os horários em que a diciplina está sendo cursada no modelo HH:MM ')
                    if verificarHora(horariosDiciplinas) == True:
                        break
                    else:
                        print('O horario digitado está no modelo errado, digite no modelo HH:MM!')
                nomeDasdiciplinas += (nomeDiciplina,)
                DadosDasDiciplinas +=(nomeDiciplina + ',' + codigoDiciplina + ',' + anoDiciplina + ',' + semestreDiciplina + ',' + horariosDiciplinas,)
                print('Diciplina criada com sucesso')
                auxCriarDiciplina = input('Deseja sair? s/n')
    return(nomeDasdiciplinas, DadosDasDiciplinas)                                           

def editarDiciplinas(nomeProfessor, nomeDasdiciplinas, DadosDasDiciplinas, listasEdicoes = []):
    while True:
        print(DadosDasDiciplinas)
        if input('Deseja listar suas diciplinas? s/n ') == 's':
            print(listarDiciplinas(nomeProfessor, nomeDasdiciplinas, DadosDasDiciplinas))
        nomeDiciplina = input('Digite o nome da diciplina que deseja editar: ')
        diciplinaExiste = False #variavel auxiliar para o for 
        DadosDiciplina = ''
        try:
            if nomeDiciplina in nomeDasdiciplinas:
                diciplinaExiste = True
                #indicar as próximas variaveis será importante mais apra a frente para reescrever as linhas de codigo
                for nome in DadosDasDiciplinas:
                    if nome.split(',')[0] == nomeDiciplina:
                        novoCodigo = nome.split(',')[1]
                        novoAno = nome.split(',')[2]
                        novoSemestre = nome.split(',')[3]
                        novoHorario = nome.split(',')[4]
                DadosDiciplina = f'Nome: {nomeDiciplina} \nCódigo: {novoCodigo} \nAno:{novoAno} \nSemestre: {novoSemestre}'

            if diciplinaExiste ==True:
                while True:
                    print(f'Nome: {nomeDiciplina} \nCódigo: {novoCodigo} \nAno:{novoAno} \nSemestre: {novoSemestre}\nHorarios: {novoHorario}')
                    print('1-Editar código \n2-Editar ano \n3-Editar período \n4-Editar Horário \n5-apagar diciplina \n6-Sair')
                    resposta = input('Digite o número desejado: ')
                    if resposta == '1':
                        novoCodigo = input('Digite o novo código desejado: ')
                    if resposta == '2':
                        novoAno = input('Digite o novo ano desejado: ')
                    if resposta == '3':
                        novoSemestre = input('Digite o novo semestre desejado: ')
                    if resposta == '4':
                        while True:
                            novoHorario = input('Digite o novo horário no modelo HH:MM')
                            if verificarHora(novoHorario) == True:
                                break
                            else:
                                print('Modelo escrito errado!')
                    if resposta == '5':
                        nomeDasdiciplinas, DadosDasDiciplinas = apagarDiciplina(nomeProfessor, nomeDiciplina, nomeDasdiciplinas, DadosDasDiciplinas)
                        break
                    if resposta == '6':
                        novaLinha = [f'{nomeDiciplina},{novoCodigo},{novoAno},{novoSemestre},{novoHorario}']
                        listasEdicoes += novaLinha
                        break
        except FileNotFoundError:
            with open(f'diciplinas{nomeProfessor}.txt', 'w'):
                print('Você não possui nenhuma diciplina cadastrada.')
                print('Voltando para o menu.')
                return
        if diciplinaExiste == False:
            print('Diciplina não encontrada')
        else:
            break
        #adicionar as edições
        print(listasEdicoes) #tirar depois
        novoArquivo = ()
        nomesEdicoes = []
        novoNomesDasDiciplinas = ()
        if listasEdicoes != []:
            for nomes in listasEdicoes:
                nomesEdicoes += [nomes.split(',')[0]]
            for nome in nomeDasdiciplinas:
                if nomeDasdiciplinas == nomeDiciplina:
                    pass
                else:
                    novoNomesDasDiciplinas += (nome,)
            for linhas in listasEdicoes:
                print(linhas) #tirar depois
                for linha in DadosDasDiciplinas:
                    if linhas.split(',')[0] == linha.split(',')[0]: #confere se os nomes são iguais
                        pass
                    else:
                        if linha not in novoArquivo and linha.split(',')[0] not in nomesEdicoes and linha != '':
                            novoArquivo += (linha,)
                novoArquivo += (linhas,)
            nomeDasdiciplinas = novoNomesDasDiciplinas
            DadosDasDiciplinas = novoArquivo
            print('arquivo editado com sucesso!')
            print(nomeDasdiciplinas)
            print(DadosDasDiciplinas)
        if input('Deseja editar outra diciplina? s/n ') != 'n':  
            pass
        else:
            break
    return nomeDasdiciplinas, DadosDasDiciplinas

def apagarDiciplina(nomeProfessor, nomeDiciplina, nomeDasdiciplinas, DadosDasDiciplinas):
    novoArquivo = ()
    novoNomesDasDiciplinas = ()
    for linha in DadosDasDiciplinas:
        if nomeDiciplina == linha.split(',')[0]:
            novoArquivo = novoArquivo
        else:
            novoArquivo += (linha,)
    for nome in nomeDasdiciplinas:
        if nomeDasdiciplinas == nomeDiciplina:
            pass
        else:
            novoNomesDasDiciplinas += (nome,)
    nomeDasdiciplinas = novoNomesDasDiciplinas
    DadosDasDiciplinas = novoArquivo
    print('arquivo editado com sucesso!')
    return nomeDasdiciplinas, DadosDasDiciplinas
    
def listarDiciplinas(nomeProfessor, nomeDasdiciplinas, DadosDasDiciplinas):
    diciplinas = ''
    for ArquivoDasDiciplinas in nomeDasdiciplinas:
        diciplinas += ArquivoDasDiciplinas + ' '
    return diciplinas
    


def mainProf(professor, path):
    os.chdir(f'{path}/Trabalho/diciplinas')
    #caso possua a caracteristica de admin ele é considerado professor
    print(f'Bem vindo {professor}')
    nomeDasDiciplinas, DadosDasDiciplinas = memoriaDiciplina(professor, path)
    NomeDasTurmas, DadosDasTurmas = memoriaTurma(professor, path)
    print(nomeDasDiciplinas, DadosDasDiciplinas)
    while True:
        menuProf()
        resposta = input('Digite o número desejado')
        if resposta == '1':
            menuDiciplina(professor, nomeDasDiciplinas, DadosDasDiciplinas, DadosDasTurmas, NomeDasTurmas, path)
            pass
        if resposta == '4':
            login()

def caminhoPastas():
    path = str(os.getcwd())
    try:
        os.makedirs(f'{path}/Trabalho')
        os.makedirs(f'{path}/Trabalho/turmas')
        os.makedirs(f'{path}/Trabalho/login')
        os.makedirs(f'{path}/Trabalho/diciplinas')
    except FileExistsError:
        pass
    return path



def memoriaTurma(nomeProfessor, path):
    DadosDasTurmas = ()
    NomeDasTurmas = ()
    os.chdir(f'{path}/Trabalho/turmas')
    try:
        arquivo = open('turma.txt','r')
        leitura = arquivo.read()
        for linha in leitura.split('\n'):
            NomeDasTurmas += (str(linha.split(',')[2]),)
            DadosDasTurmas += (str(linha),)
            return NomeDasTurmas, DadosDasTurmas
    except FileNotFoundError:
        with open('turma.txt','w'):
            return NomeDasTurmas, DadosDasTurmas
        


def memoriaDiciplina(nomeProfessor, path):
    os.chdir(f'{path}/Trabalho/diciplinas')
    nomesDasDiciplinas = ()
    DadosDasDiciplinas = ()
    try:
        arquivo = open(f'diciplinas{nomeProfessor}.txt', 'r')
        leitura = arquivo.read()
        for linha in leitura.split('\n'):
            nomesDasDiciplinas+= (str(linha.split(',')[0]),)
            DadosDasDiciplinas += (str(linha),)
        arquivo.close()
        return nomesDasDiciplinas, DadosDasDiciplinas
    except FileNotFoundError:
        with open(f'diciplinas{nomeProfessor}.txt', 'w'):
            return nomesDasDiciplinas, DadosDasDiciplinas

def Start():
    path = caminhoPastas()
    login(path)

Start()
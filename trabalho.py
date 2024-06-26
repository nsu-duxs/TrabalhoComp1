import hashlib
import os
def menuProf():
    print('1- Editar diciplina') #adicionar outro sub menu dps com editar codigo, nome, ano, turmas
    print('2- Editar aluno')
    print('3- logout')
#---------------------------------------LOGIN----------------------------------------------------------------------------
def login(path = str(os.getcwd())):
    os.chdir(f'{path}/Trabalho/login')
    try:
        arquivoLogin = open('login.txt', 'r+')
        leitura = arquivoLogin.read()
        print('Digite: \n 1- Fazer login \n 2- Criar nova conta')
        resposta = input('Digite: ')
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
                                if linha.split(',')[2] == 'admin':
                                    mainProf(nome, path)
                                if linha.split(',')[2] == 'aluno':
                                    mainAluno(nome, path)
                                    pass
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
                            print('Esse nome já está sendo usado faça login ou crie uma conta com outro nome: ')
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
                                arquivoLogin.write(hashlib.sha256(senha.encode()).hexdigest() +',aluno' + '\n')
                                adicionarAluno(nome, path)

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
        
#--------------------------------------------Diciplinas----------------------------------------------------------------------------------------------------

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

def salvarArquivosAluno(DadosAlunos, path):
    os.chdir(f'{path}/Trabalho/turmas/alunos')
    arquivo = open('alunos.txt', 'w')
    for linha in DadosAlunos:
        if linha != '':
            arquivo.write(linha + '\n')
    arquivo.close()


def CriarTurmas(nomeProfessor, nomeDasdiciplinas,DadosDasTurmas, NomeDasTurmas):
    while True:
        diciplina = input('Digite o nome da diciplina: ')
        if diciplina in nomeDasdiciplinas:
            nomeTurma = input('Digite o nome da turma que deseja criar: ')
            if nomeTurma in NomeDasTurmas:
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
                while True:
                    pesoAvaliacaoTurma = input('Digite os pesos das avaliações EX: se digitou p1+p2, agor digite 1+2(O peso da p2 é o dobro do peso da p1): ')
                    if verificarPesos(formaAvaliacaoTurma, pesoAvaliacaoTurma) == True:
                        break
                    
                DadosDasTurmas += (nomeProfessor+ ',' + diciplina + ',' + nomeTurma + ',' + codigoTurma + ',' + horarioTurma + ',' + formaAvaliacaoTurma + ',' + pesoAvaliacaoTurma,)
                NomeDasTurmas += (nomeTurma,)
                if input('Deseja criar outra turma? s/n ') != 'n':
                    pass
                else:
                    break
        else:
            print('Diciplina não encontrada!')
            if input('deseja sair? s/n') != 'n':
                break
    return NomeDasTurmas, DadosDasTurmas

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
    
def verificarPesos(FormaAvaliacaoTurma, PesoAvaliacaoTurma):
    numeroProvas = 0
    numeroPesos = 0
    for n in FormaAvaliacaoTurma.split('+'):
        numeroProvas += 1
    try: 
        for n in  PesoAvaliacaoTurma.split('+'):
            numeroPesos +=1
            if type(int(n)) == int:
                pass
            else:
                raise ValueError
    except ValueError:
        print( 'Você deve digitar apenas numeros inteiros separados por <+>')
        return False
    if numeroPesos == numeroProvas and numeroProvas > 0 and numeroPesos > 0:
        return True
    else: 
        print('O formato inserido está errado, digite números inteiros separados por <+> igual ao numero de avaliações')
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
                    novoPeso = nome.split(',')[6]
        if TurmaExiste == True:
            while True:  
                print(f'Nome: {nomeTurma}\nCódigo: {novoCodigo}\nHorário:{novoHorario}\nModelo Avaliativo:{novaAvaliacoes}')        
                print('Digite o número de acordo com o que você deseja editar: \n1-Código \n2-Horario \n3-Avaliações e Pesos\n4-Apagar Turma\n7-Sair')
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
                    while True:
                        novoPeso = input('Digite os novos pesos no mesmo modelo, separando por <+>')
                        if verificarPesos(novaAvaliacoes, novoPeso) == True:
                            break
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
    while True:
        nomeDasDiciplinas, DadosDasDiciplinas = memoriaDiciplina(professor, path)
        NomeDasTurmas, DadosDasTurmas = memoriaTurma(path)
        nomesAlunos, DadosAlunos = memoriaAlunos(path)
        print(nomesAlunos, DadosAlunos)
        menuProf()
        resposta = input('Digite o número desejado')
        if resposta == '1':
            menuDiciplina(professor, nomeDasDiciplinas, DadosDasDiciplinas, DadosDasTurmas, NomeDasTurmas, path)
            pass
        if resposta == '2':
            MenuAlunos(DadosDasTurmas, NomeDasTurmas, nomesAlunos, DadosAlunos, path)
        if resposta == '3':
            login()

def caminhoPastas():
    path = str(os.getcwd())
    try:
        os.makedirs(f'{path}/Trabalho')
        os.makedirs(f'{path}/Trabalho/turmas')
        os.makedirs(f'{path}/Trabalho/turmas/avaliacoes')
        os.makedirs(f'{path}/Trabalho/turmas/alunos')
        os.makedirs(f'{path}/Trabalho/login')
        os.makedirs(f'{path}/Trabalho/diciplinas')
    except FileExistsError:
        pass
    return path



def memoriaTurma(path):
    DadosDasTurmas = ()
    NomeDasTurmas = ()
    os.chdir(f'{path}/Trabalho/turmas')
    try:
        arquivo = open('turma.txt','r')
        leitura = arquivo.read()
        for linha in leitura.split('\n'):
            try:
                NomeDasTurmas += (str(linha.split(',')[2]),)
                DadosDasTurmas += (str(linha),)
            except:
                pass
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

#--------------------------------------AVALIAÇÕES-----------------------------------------------------
def memoriaAvaliacoes(nomeProfessor, path):
    os.chdir(f'{path}/Trabalho/turmas/avaliacoes')
    calculoAvaliacao = ()
    try:
        arquivo = open('avaliacoes.txt', 'r')
        leitura = arquivo.read()
        for linha in leitura.split('\n'):
            calculoAvaliacao += (str(linha),)
        arquivo.close()
        return calculoAvaliacao
    except FileNotFoundError:
        with open('avaliacoes.txt', 'w'):
            return calculoAvaliacao
        
#def menuAvaliacoes(NomeProfessor, DadosDasTurmas, DadosAvaliações):
    
#---------------------------------------ALUNOS------------------------------------------------
def memoriaAlunos(path):
    os.chdir(f'{path}/Trabalho/turmas/alunos')
    nomesAlunos = ()
 #notas vao ser dadas nesse sentido = dict {nomeTurma:nota}
    DadosAlunos = ()
    try:
        arquivo = open('alunos.txt', 'r')
        leitura = arquivo.read()
        for linha in leitura.split('\n'):
            nomesAlunos += (linha.split(';')[0],)
            DadosAlunos += (linha,)
        return nomesAlunos, DadosAlunos
    except FileNotFoundError:
        with open('alunos.txt', 'w'):
            return nomesAlunos, DadosAlunos
#NomeAluno,{nomeTurma:nota, nomeTurma2:nota},{frequenciaTurma:int, frequenciaTurma2:int}
def MenuAlunos(DadosDasTurmas, NomeDasTurmas, nomesAlunos, DadosAlunos, path):
    while True:
        os.chdir(f'{path}/Trabalho/turmas/alunos')
        print('1-Cadastrar Aluno em turma\n2-Adicionar notas\n3-Editar frequência\n4-Salvar e sair')
        resposta = input('digite a função desejada: ')
        if resposta == '1':
            nomesAlunos, DadosAlunos = CadastrarAluno(DadosDasTurmas, NomeDasTurmas, nomesAlunos, DadosAlunos, path, [])
        if resposta == '2':
            nomesAlunos, DadosAlunos = EditarNotas(DadosDasTurmas, NomeDasTurmas, nomesAlunos, DadosAlunos, path, [])
            pass
        if resposta == '3':
            nomesAlunos, DadosAlunos = EditarFrequencia(DadosDasTurmas, NomeDasTurmas, nomesAlunos, DadosAlunos, path, [])
        if resposta == '4':
            salvarArquivosAluno(DadosAlunos, path)
            break

def CadastrarAluno(DadosDasTurmas, NomeDasTurmas, nomesAlunos, DadosAlunos, path, listasEdicoes = []):
    if input('deseja listar seus alunos? s/n: ') == 's':
        print(nomesAlunos)
        print(DadosAlunos)
    aluno_nome = input('digite o nome do aluno desejado: ').upper()
    if aluno_nome in nomesAlunos:
        for nome in DadosAlunos:
            if aluno_nome == nome.split(';')[0]:        
                novaNota = eval(nome.split(';')[1])
                novoFrequencia = eval(nome.split(';')[2])
        print(novaNota)
        print(novoFrequencia)
        while True:
            turma = input('Digite o nome da turma desejada: ')
            if turma in NomeDasTurmas:
                for nome in DadosAlunos:
                    if aluno_nome == nome.split(';')[0]:
                        novaNota[turma] = 0
                        novoFrequencia[turma] = 0
                novaLinha = [f'{aluno_nome.upper()};{novaNota};{novoFrequencia}']
                listasEdicoes += novaLinha  
                break     
            else:
                print('turma não encontrada!')         
        #continuar
        novoArquivo = ()
        nomesEdicoes = []
        novoNomeDosAlunos = ()
        if listasEdicoes != []:
            for nomes in listasEdicoes:
                nomesEdicoes += [nomes.split(';')[0]]
            for nome in nomesAlunos:
                if nomesAlunos == aluno_nome:
                    pass
                else:
                    novoNomeDosAlunos += (nome,)
            for linhas in listasEdicoes:
                for linha in DadosAlunos:
                    if linhas.split(';')[0] == linha.split(';')[0]:
                        pass
                    else:
                        if linha not in novoArquivo and linha.split(';')[0] not in nomesEdicoes and linha != '':
                            novoArquivo+=(linha,)
                novoArquivo +=(linhas,)
            nomesAlunos = novoNomeDosAlunos
            DadosAlunos = novoArquivo
            print('arquivo editado!')
            print(f"nomes alunos:  {nomesAlunos}")
            print(f'Dados Alunos:  {DadosAlunos}')
    else:
        print('Aluno não encontrado, saindo..')
    return nomesAlunos, DadosAlunos

def IsInt(n):
    try:
        if type(int(n)) == int:
            return True
        else:
            return False
    except ValueError:
        return False               

def EditarFrequencia(DadosDasTurmas, NomeDasTurmas, nomesAlunos, DadosAlunos, path, listasEdicoes = []):
    if input('deseja listar seus alunos? s/n: ') == 's':
        print(nomesAlunos)
        print(DadosAlunos)
    aluno_nome = input('digite o nome do aluno desejado: ').upper()
    if aluno_nome in nomesAlunos:
        for nome in DadosAlunos:
            if aluno_nome == nome.split(';')[0]:        
                novaNota = eval(nome.split(';')[1])
                novoFrequencia = eval(nome.split(';')[2])
        while True:
            turma = input('Digite o nome da turma desejada: ')
            if turma in NomeDasTurmas and turma in novoFrequencia:
                while True:
                    frequencia = input('Digite a frequencia do aluno: ')#ainda tem que conferir se é INT
                    if IsInt(frequencia) == True:
                        break
                    else:
                        pass
                for nome in DadosAlunos:
                    if aluno_nome == nome.split(';')[0]:
                        novoFrequencia[turma] = int(frequencia)
                novaLinha = [f'{aluno_nome.upper()};{novaNota};{novoFrequencia}']
                listasEdicoes += novaLinha
                break     
            else:
                print('turma não encontrada ou o aluno não está cadastrado nela!')
                if input('Deseja continuar? s/n: ') == 'n':
                    break
        #continuar
        novoArquivo = ()
        nomesEdicoes = []
        novoNomeDosAlunos = ()
        if listasEdicoes != []:
            for nomes in listasEdicoes:
                nomesEdicoes += [nomes.split(';')[0]]
            for nome in nomesAlunos:
                if nomesAlunos == aluno_nome:
                    pass
                else:
                    novoNomeDosAlunos += (nome,)
            for linhas in listasEdicoes:
                for linha in DadosAlunos:
                    if linhas.split(';')[0] == linha.split(';')[0]:
                        pass
                    else:
                        if linha not in novoArquivo and linha.split(';')[0] not in nomesEdicoes and linha != '':
                            novoArquivo+=(linha,)
                novoArquivo +=(linhas,)
            nomesAlunos = novoNomeDosAlunos
            DadosAlunos = novoArquivo
            print(f"nomes alunos:  {nomesAlunos}")
            print(f'Dados Alunos:  {DadosAlunos}')
    return nomesAlunos, DadosAlunos


def EditarNotas(DadosDasTurmas, NomeDasTurmas, nomesAlunos, DadosAlunos, path, listasEdicoes = []):
    if input('deseja listar seus alunos? s/n: ') == 's':
        print(nomesAlunos)
        print(DadosAlunos)
    aluno_nome = input('digite o nome do aluno desejado: ').upper()
    if aluno_nome in nomesAlunos:
        for nome in DadosAlunos:
            if aluno_nome == nome.split(';')[0]:        
                novaNota = eval(nome.split(';')[1])
                novoFrequencia = eval(nome.split(';')[2])
        while True:
            turma = input('Digite o nome da turma desejada: ')
            if turma in NomeDasTurmas and turma in novaNota:
                while True:
                    notas = input('Digite as novas notas do aluno separadas por <+>: ')
                    AuxiliarDaVerificao, notas = verificarNota(DadosDasTurmas, turma, notas)
                    print(notas)
                    if AuxiliarDaVerificao == True:
                        break
                    else:
                        print('Os numeros inseridos devem ser inteiros e separados com <+> na mesma quantidade de provas, se você deseja inserir apenas 1 das notas coloque as restantes como 0')
                
                for nome in DadosAlunos:
                    if aluno_nome == nome.split(';')[0]:
                        novaNota[turma] = notas #nota Com peso
                novaLinha = [f'{aluno_nome.upper()};{novaNota};{novoFrequencia}']
                listasEdicoes += novaLinha
                break       
            else:
                print('turma não encontrada ou o aluno não está cadastrado nela!')
                if input('Deseja continuar? s/n: ') == 'n':
                    break
        #continuar
        print(listasEdicoes)
        novoArquivo = ()
        nomesEdicoes = []
        novoNomeDosAlunos = ()
        if listasEdicoes != []:
            for nomes in listasEdicoes:
                nomesEdicoes += [nomes.split(';')[0]]
            for nome in nomesAlunos:
                if nomesAlunos == aluno_nome:
                    pass
                else:
                    novoNomeDosAlunos += (nome,)
            for linhas in listasEdicoes:
                for linha in DadosAlunos:
                    if linhas.split(';')[0] == linha.split(';')[0]:
                        pass
                    else:
                        if linha not in novoArquivo and linha.split(';')[0] not in nomesEdicoes and linha != '':
                            novoArquivo+=(linha,)
                novoArquivo +=(linhas,)
            nomesAlunos = novoNomeDosAlunos
            DadosAlunos = novoArquivo
            print(f"nomes alunos:  {nomesAlunos}")
            print(f'Dados Alunos:  {DadosAlunos}')
    return nomesAlunos, DadosAlunos

def adicionarAluno(nome, path):
    os.chdir(f'{path}/Trabalho/turmas/alunos')
    notas = {}
    frequencia = {}
    try:
        arquivo = open('alunos.txt', 'a')
        arquivo.write(nome+ f';{notas};{frequencia}'+'\n')
    except FileNotFoundError:
        arquivo = open('alunos.txt','w')
        arquivo.write(nome+ f';{notas};{frequencia}'+'\n')
        arquivo.close()

def verificarNota(DadosDasTurmas, turma, notas):
    numeroProvas = 0
    numeroNotas = 0
    pesos = ''
    listaPesos = []
    listasNotas = []
    notaFinal = 0
    for nome in DadosDasTurmas:
        if turma == nome.split(',')[2]:
            for provas in nome.split(',')[5].split('+'):
                numeroProvas +=1
            pesos = nome.split(',')[6]
    for x in pesos.split('+'):
        listaPesos +=[int(x)]
    for n in notas.split('+'):
        numeroNotas +=1
        try:
            listasNotas += [float(n)]
        except ValueError:
            print('O numero inserido não é um inteiro')
            return False, 0
    if numeroNotas == numeroProvas:
        notaFinal = 0
        media = 0
        for n in range(numeroNotas):
            notaFinal += listaPesos[n] * listasNotas[n]
            media += listaPesos[n]
        Resposta = notaFinal/media
        return True, Resposta
    else:
        print(f'Você deve digitar {numeroProvas} numeros separados por <+>')
        return False, 0
    
    


def mainAluno(nome, path):
    while True:
        nomeAlunos, DadosAlunos = memoriaAlunos(path)
        nomeDasTurmas, DadosDasTurmas = memoriaTurma(path) 
        print('1-Ver notas\n 2-ver calculo\n 3-Ver frequencia \n 4-calculo aprovação')
        resposta = input('Digite a opção desejada: ')
        if resposta == '1':
            mostrarNotas(nome, DadosAlunos)
        if resposta == '2':
            CalculoProvas(nome, DadosAlunos, DadosDasTurmas)
        if resposta == '3':
            mostrarFrequencia(nome, DadosAlunos)

def mostrarNotas(nomeAluno, DadosAlunos):
    for nome in DadosAlunos:
        if nomeAluno == nome.split(';')[0]:
            for turmas in nome.split(';')[1].split(','):
                print(turmas.strip('{}').replace("'", "")) #remove os conchetes e os apostrofos para facilitar o codigo

def CalculoProvas(nomeAlunos, DadosAlunos, DadosDasTurmas):
    numProvas = 0
    Provas = ''
    Pesos = ''
    listasPesos = []
    listasProvas = []
    listaturmas = []
    media = 0
    for nome in DadosAlunos:
        if nomeAlunos == nome.split(';')[0]:
            dicionarioTurmas = eval(nome.split(';')[1])
            print('Essas São as suas turmas inscritas: ', end='')
            listaturmas = list(dicionarioTurmas.keys())
            print(list(dicionarioTurmas.keys()))
    while True:
        TurmasDesejada = input('Digite o nome da turma que deseja editar: ')
        if TurmasDesejada in listaturmas:
            break
        else:
            print('Esta turma não exite ou você não esté inscrito nela')
    for notas in DadosDasTurmas:
        if notas.split(',')[2] == TurmasDesejada:
            Provas = notas.split(',')[5]
            Pesos = notas.split(',')[6]
    for p in Provas.split('+'):
        numProvas +=1
        listasProvas += [p]
    for peso in Pesos.split('+'):
        listasPesos += [int(peso)]
        media += int(peso)
    print(f'Esta turma é avaliada em {numProvas} para calcular sua nota é feito o seguinte calculo: ')
    for peso in range(len(listasProvas)):
        print(f'({listasProvas[peso]}*{listasPesos[peso]})',end='')
        if peso != len(listasProvas)-1:
            print('+', end='')
    print(f'/{media}')
    return 
    


def mostrarFrequencia(nomeAluno, DadosAlunos):
    for nome in DadosAlunos:
        if nomeAluno == nome.split(';')[0]:
            for turmas in nome.split(';')[2].split(','):
                print(turmas.strip('{}').replace("'", "")) #remove os conchetes e os apostrofos para facilitar o codigo
    


    



#---------------------------------------START--------------------------------------------------------
def Start():
    path = caminhoPastas()
    login(path)

Start()


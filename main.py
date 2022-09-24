import csv

objnomes = ["id", "setor", "obj", "responsavel", "ano", "ciclo"]
krsnomes = ['id', 'setor', 'texto', 'tipo', 'inicial', 'mudar', 'meta', 'responsavel', 'arquivado']

objetivo = []
krs = []

id_objetivo = 0
nkr = 0
id_kr = 0
appon = True

while appon:
    acao = input("Escolha a ação que deseja: registrar/atualizar/check-in/acompanhar: ")
    if acao == 'off':
        appon = False

    if acao == 'registrar':
        id_objetivo += 1
        setor = input('Qual o seu setor? ')
        texto = input("Qual o seu objetivo? ")
        responsavel = input("Quem é responsável? ")
        ano = int(input("Qual o ano de vigência do OKR? "))
        ciclo = int(input("Qual o trimestre? "))
        if ciclo > 4:
            ciclo = 4
        objetivo = [id_objetivo, setor, texto, responsavel, ano, ciclo]
        print(objetivo)

        with open('objetivo.csv', 'a') as file:
            write = csv.writer(file)
            write.writerows(objetivo)

        nkrs = int(input("quantos Kr's deseja registrar? "))

        for i in range(nkrs):
            id_kr += 1
            texto = input("Qual o seu KR? ")
            tipo = input("Qual o tipo do KR?[a/d/m] ")
            operando = input("valor absoluto ou porcentage?[a/p] ")
            inicial = int(input("Qual o valor inicial do KR? "))
            mudar = int(input("Quanto o KR deve mudar? "))
            meta = 0
            if tipo == 'aumentar':
                if operando == 'a':
                    meta = inicial + mudar
                elif operando == 'p':
                    meta = inicial * (1 + mudar / 100)
            elif tipo == 'diminuir':
                if operando == 'a':
                    meta = inicial - mudar
                elif operando == 'p':
                    meta = inicial * (mudar / 100)
            elif tipo == 'milestone':
                if operando == 'a':
                    meta = inicial + mudar
                elif operando == 'p':
                    meta = 100
            responsavel = input("Quem é o responsável?")
            krs = [id_kr,id_objetivo, setor, texto, tipo, operando, inicial, mudar, meta, responsavel]
            print(krs)
            with open('okr.csv', 'a') as file:
                write = csv.writer(file)
                write.writerow(krsnomes)
                write.writerows(krs)

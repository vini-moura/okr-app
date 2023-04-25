from pandas import *

class Okr:
    def __init__(self, id_user, user, id_time, time):
        self.id_user = id_user
        self.user = user
        self.id_time = id_time
        self.time = time

    def cadastrar_okr(self, obj, setor, texto, responsavel, ano, trimestre):
        """cadastra novo objetivo + n krs vinculados ao mesmo"""
        novo_id = obj['id_obj'].iloc[-1] + 1
        novo_obj = DataFrame([novo_id, self.id_time, self.time, id_setor, setor, texto, responsavel, ano, trimestre])
        print(novo_obj)
        novo_obj.to_csv("static/okr.csv", mode='a', header=False, index=False)

        n = int(input("\nQuantos KRs serão associados a este Objetivo?  "))
        for i in range(0, n):
            id_obj = novo_id
            id_kr = krs['id_kr'].iloc[-1] + 1
            texto = input("\nDigite o texto do KR:  ")
            tipo = input("Digite o tipo de KR [a/d/m]:  ")
            un_medida = input("Número absoluto ou porcentagem? [a/p]  ")
            inicial = int(input("Digite o número inicial do KR:  "))
            valor_alterar = int(input("Digite o valor a alterar:  "))
            status = 'novo'
            meta = 0
            atual = ''
            if tipo == 'a' and un_medida == 'a':
                meta = inicial + valor_alterar
            elif tipo == 'a' and un_medida == 'p':
                meta = inicial + (inicial * valor_alterar / 100)
            elif tipo == 'd' and un_medida == 'a':
                meta = inicial - valor_alterar
            elif tipo == 'd' and un_medida == 'p':
                meta = inicial - (inicial * valor_alterar / 100)
            elif tipo == 'm' and un_medida == 'a':
                meta = valor_alterar
            elif tipo == 'm' and un_medida == 'p':
                meta = 100

            novo_kr = DataFrame([id_kr, id_obj, texto, tipo, un_medida, inicial, valor_alterar, meta, status, atual]).T
            novo_kr.to_csv("static/krs.csv", mode='a', header=False, index=False)
            print(f'\n{novo_kr}')

    def atualizar_kr(self, obj, krs, trimestre, ano):
        """atualiza os 3Ps + valor atual do kr selecionado"""

        ligado = True
        while ligado:

            obj2 = obj[(obj['ciclo'] == trimestre) & (obj['ano'] == ano)]
            print('\nEstes são os objetivos disponíveis para atualização:')
            print(obj2[['id_obj', 'texto']])
            id_obj = int(input('Qual objetivo deseja atualizar? [id_obj]  '))
            krs = krs[krs['id_obj'] == id_obj]

            # atualiza os kr do mesmo obj até usuario encerrar
            ligado2 = True
            while ligado2:
                # seleciona um kr e insere 3p's.
                print("\nEstes são os KR's deste objetivo:")
                print(krs[['id_kr', 'texto', 'inicial', 'meta', 'atual']])
                kr_desejado = int(input('Qual KR deseja atualizar? [id_kr]  '))
                ppp = input("Algum progresso, problema ou plano?:  ")

                atualizacoes = read_csv('static/atualizacoes.csv')
                # se kr_desejado já tem atualização, mostra ultima mudança. Se não tem, mostra valor inicial
                if kr_desejado in atualizacoes[['id_kr']].values:
                    atual = atualizacoes.loc[atualizacoes['id_kr'] == kr_desejado, "atual"].values
                    print(atual)
                else:
                    atual = krs.loc[krs['id_kr'] == kr_desejado]["inicial"].values[0]
                    print(atual)
                meta = krs.loc[krs['id_kr'] == kr_desejado, 'meta'].tolist()

                # variavel 'novo_valor' é o valor atual do kr. Pergunta se o user quer alterar e atualiza
                novo_valor = atual
                mudou = input(f"\nO valor atual do kr é: {atual} com meta de {meta[0]}. Deseja mudar? [s/n]  ")
                if mudou == 's':
                    novo_valor = input("Qual o novo valor?  ")
                krs.loc[krs['id_kr'] == kr_desejado, 'atual'] = novo_valor
                if kr_desejado in atualizacoes[['id_kr']].values:
                    krs.loc[krs['id_kr'] == kr_desejado, 'status'] = 'iniciado'

                krs.to_csv('static/krs.csv', index=False)

                novo_id = atualizacoes['id_atualizacao'].iloc[-1] + 1
                atualizacao = DataFrame([novo_id, self.id_user, self.user, id_obj, kr_desejado, ppp, novo_valor]).T
                atualizacao.to_csv('static/atualizacoes.csv', mode='a', header=False, index=False)

                mais_um2 = input('Deseja atualizar mais um KR desse Objetivo? [s/n]  ')
                if mais_um2 == 'n' or mais_um2 == 'nao' or mais_um2 == 'não':
                    ligado2 = False

                """          fim do loop para KR          """

            mais_um = input("Deseja atualizar outro OKR?  ")
            if mais_um == 'n' or mais_um == 'nao' or mais_um == 'não':
                ligado = False

    def monitorar_okr(self, obj, krs, trimestre, ano):

        """imprime os okrs junto com os krs, caso estejam no trimestre e ano atual """

        aobj = obj[(obj['ciclo'] == trimestre) & (obj['ano'] == ano)]
        ids = aobj['id_obj'].to_list()

        akrs = DataFrame()
        for label, row in krs.iterrows():
            if row['id_obj'] in ids:
                akrs[len(akrs)] = row
        akrs = akrs.T

        n = 0
        for l, r in aobj.iterrows():
            n += 1
            print(f"\n\nObjetivo {n}:")
            print(r[['time', 'setor', 'texto', 'responsavel']].to_frame().T)
            id_esp = int(r[['id_obj']])
            print('KRs:')
            c = akrs[akrs['id_obj'] == id_esp].reset_index(drop=True)
            print(c[['texto', 'tipo', 'inicial', 'meta', 'atual']], '\n\n')

    def corrigir(obj, krs):
        pass
import pandas as pd
from datetime import date


class Cerebro:
    def __init__(self):
        self.hoje = date.today()
        self.trimestre = 0
        self.id_user = ""
        self.user = ""
        self.id_time = ""
        self.time = ""
        self.aobj = ''
        self.progresso_geral = 0

    def ciclodef(self):
        if 1 <= self.hoje.month <= 3:
            self.trimestre = 1
        elif 4 <= self.hoje.month <= 6:
            self.trimestre = 2
        elif 7 <= self.hoje.month <= 9:
            self.trimestre = 3
        else:
            self.trimestre = 4

    def entrada(self, nome, senha):
        usuarios = pd.read_csv("/home/viniciusmoura/mysite/static/users.csv")
        desejado = usuarios[usuarios['user'] == nome]

        if senha in desejado["senha"]:
            self.id_user = desejado["id_user"]
            self.user = nome
            self.id_time = desejado['id_time']
            self.time = desejado['time']
            return True
        
    def monitorar(self):
        krs = pd.read_csv("/home/vinicius/PycharmProjects/okr/static/krs.csv")
        obj = pd.read_csv("/home/vinicius/PycharmProjects/okr/static/okr.csv")
        aobj = obj[(obj['ciclo'] == self.trimestre) & (obj['ano'] == self.hoje.year)]
        akrs = krs[krs['id_obj'].isin(aobj['id_obj'])]
        # aobj.to_csv("/static/teste.csv")
        self.progresso_geral = akrs['%'].mean()

        return aobj, akrs

    def atualiza(self, setor, okr, kr, ppp, valor):
        obj = pd.read_csv("/home/viniciusmoura/mysite/static/okr.csv")
        krs = pd.read_csv("/home/viniciusmoura/mysite/static/krs.csv")
        atualiza = pd.read_csv("/home/viniciusmoura/mysite/static/atualizacoes.csv")

        novoId = atualiza["id_atualiza]"].iloc[-1] + 1

        #d_atualiza,id_obj,id_kr,texto,tipo,un_medida,inicial,valor_alterar,meta,ppp,atual,%

        pass

    def cadastrar(self, setor, texto, ano, trimestre):
        obj = pd.read_csv("/home/vinicius/PycharmProjects/okr/static/okr.csv")
        novoId = obj["id_obj"].iloc[-1] + 1
        novaLinha = [novoId, self.id_time, self.time, setor, texto, self.user, ano, trimestre]
        obj[len(obj)] = novaLinha
        obj.to_csv("/home/vinicius/PycharmProjects/okr/static/okr.csv", index=False)

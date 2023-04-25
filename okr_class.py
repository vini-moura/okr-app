class User:
    def __init__(self, id1,nome,time,email):
        self.id = id1
        self.nome = nome
        self.time = time
        self.email =email

class Objetivo:
    def __init__(self, id1,time,setor,obj,responsavel,ano,ciclo):
        self.id = id1
        self.time = time
        self.setor= setor
        self.texto = obj
        self.responsavel = responsavel
        self.ano = ano
        self.ciclo = ciclo

class ResultadoChave:
    def __init__(self, id1, num, id_obj, setor, texto, tipo, inicial, mudar, meta, responsavel, status, atual, p):
        self.id1 = id1
        self.num= num
        self.id_obj = id_obj
        self.setor = setor
        self.texto = texto
        self.tipo = tipo
        self.inicial = inicial
        self.mudar = mudar
        self.meta = meta
        self.responsavel = responsavel
        self.status = status
        self.atual = atual
        self.p = p

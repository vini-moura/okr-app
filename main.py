#caroline.yamazato@ufms.br

from okr import *
from users import *
from ciclo import *
from pandas import *

print("Bem vindo ao app okr por vinicius oliveira\n")

on = True
while on:
    escolha = input("Digite 1 para fazer login, 2 para cadastrar novo usuário ou 3 para sair:  ")

    if escolha == '1':
        usuario = login()

        while usuario != 0:
            obj = read_csv('static/okr.csv')
            krs = read_csv("static/krs.csv")
            t_u = read_csv('static/times_users.csv')

            a = t_u[t_u['id_user'] == usuario].values.flatten().tolist()

            o = Okr(usuario, a[2], a[0], a[1])
            c = Ciclo()
            c.ciclo_def()

            obj_f = obj[obj['id_time'] == o.id_time]
            b = krs.id_obj.isin(obj_f.id_obj)
            krs_f = krs[b]

            acao = input("\nDigite 1 para cadastrar, 2 para atualizar e 3 para monitorar um OKR:  ")

            if acao == "1":
                o.cadastrar_okr(obj, krs)
            elif acao == "2":
                o.atualizar_kr(obj_f, krs_f, c.trimestre, c.ano)
            elif acao == "3":
                o.monitorar_okr(obj_f, krs_f, c.trimestre, c.ano)
            elif acao == "sair" or acao == 'exit' or acao == 's' or acao == 'e' or acao == '4':
                usuario = 0

            else:
                pass

    elif escolha == '2':
        cadastro()

    elif escolha == '3':
        on = False

    else:
        pass
import json
from okr_class import *


with open('json/obj.json','r') as f:
    obj = json.load(f)
with open('json/users.json','r') as f:
    user = json.load(f)
with open('json/resultadoschave.json','r') as f:
    rcs = json.load(f)


nome = 'vinicius oliveira'
log_user = [i for i in user if i['nome'] in nome]
times = [i['time'] for i in user if i['nome'] in nome]
selecionados = [i for i in obj if i['time'] in times]

usuario = []
for u in log_user:
    a = User(u['id'],u['nome'],u['time'],u['time'])
    usuario.append(a)

print(usuario.time)

objetivos = []
for o in selecionados:
    # id,time,setor,obj,responsavel,ano,ciclo
    a = Objetivo(o['id'],o['time'],o['setor'],o['obj'],o['responsavel'],o['ano'],o['ciclo'])
    objetivos.append(a)

rc_selecionados = [i for i in rcs if i['id_obj'] in selecionados]

krs = []
for rc in rcs:
    #id1, id_obj, setor, texto, tipo, inicial, mudar, meta, responsavel, status, atual, p
    a = ResultadoChave(rc['id'],    rc['id_obj'],
                       rc['setor'],     rc['texto'],
                       rc['tipo'],      rc['inicial'],
                       rc['mudar'],     rc['meta'],
                       rc['responsavel'],   rc['status'],
                       rc['atual'],     rc['p'])
    krs.append(a)

media_total = 32

# user_log= 'vinicius oliveira'
#
# times_log = [i['time'] for i in user if i['nome'] in user_log]
# obj_log = [i for i in obj if i['time'] in times_log]
#
# obj_mostrar = []
# for o in obj_log:
#     # id1,time,setor,obj,responsavel,ano,ciclo
#     a = Objetivo(o['id'],o['time'],o['setor'],o['obj'],o['responsavel'],o['ano'],o['ciclo'])
#     obj_mostrar.append(a)
#
#
# print(obj_mostrar[0].obj)





# for i in user:
#     a = user[i][user[i]['time'] == user_log]
#     obj_log.extend(a)


# user_log = 'vinicius oliveira'
# time_log = user['time'][user['nome'] == user_log]


# obj_log = []
# for i in obj:
#     a = obj[obj['time'] == i].to_dict()
#     print(a)
#     b = Objetivo(a['id'],a['time'],a['setor'],a['obj'],a['responsavel'],a['ano'],a['ciclo'])
#     obj_log.append(b)
#
# print(obj_log[0].obj.to_string())

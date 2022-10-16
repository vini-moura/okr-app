from flask import Flask, render_template
from okr_class import *
import json


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


# -------------------------

app= Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html",
                           media_total = media_total,
                           objetivos = objetivos,
                           krs = krs,
                           usuario= usuario)
#
if __name__ == '__main__':
    app.run(debug=True)

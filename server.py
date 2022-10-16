from flask import Flask, render_template
from okr_class import *
import json

with open('json/obj.json', 'r') as f:
    file_obj = json.load(f)
with open('json/users.json', 'r') as f:
    file_user = json.load(f)
with open('json/resultadoschave.json', 'r') as f:
    file_rcs = json.load(f)

nome = 'vinicius oliveira'
log_user = [i for i in file_user if i['nome'] in nome]
list_time = [i['time'] for i in file_user if i['nome'] in nome]
times = [i for group in list_time for i in group]
selecionados = [i for i in file_obj if i['time'] in times]


usuario = [User(u['id'], u['nome'], u['time'], u['time']) for u in log_user]

objetivos = [Objetivo(o['id'], o['time'], o['setor'], o['obj'], o['responsavel'], o['ano'], o['ciclo']) for o in
             selecionados]
ids_obj = [o['id'] for o in selecionados]


rc_selecionados = [i for i in file_rcs if i['id_obj'] in ids_obj]
krs = []
for rc in rc_selecionados:
    # id1, id_obj, setor, texto, tipo, inicial, mudar, meta, responsavel, status, atual, p
    a = ResultadoChave(rc['id'], rc['id_obj'],
                       rc['setor'], rc['texto'],
                       rc['tipo'], rc['inicial'],
                       rc['mudar'], rc['meta'],
                       rc['responsavel'], rc['status'],
                       rc['atual'], rc['p'])
    krs.append(a)


media_total = 0
for i in krs:
    media_total += i.atual


# -------------------------

app= Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", media_total = media_total, objetivos = objetivos, krs = krs, usuario= usuario)

if __name__ == '__main__':
    app.run(debug=True)

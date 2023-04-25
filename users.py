from pandas import *
import maskpass
#from okr import *

'''
class Usuario:
  def __init__(self):
    self.id = ''
    self.nome = ''
    self.time_id = ''
    self.time = ''
    self.email = ''
    self.senha = ''
  '''


def cadastro():
    users = read_csv('static/users.csv')
    novo_id = users['id_user'].iloc[-1] + 1

    email = input("\n\nDigite seu email:  ")
    usuario = input("Digite seu nome de usuário:  ")
    senha = input("Digite sua senha:  ")
    conf_senha = input("Confirme sua senha:  ")
    if conf_senha == senha:
        new_user = [novo_id, usuario, email, senha]
        users.loc[len(users)] = new_user
        users.to_csv("static/users.csv", index=False)
        print("\n\nCadastro realizado com sucesso!\n\n")
    else:
        print("\n\nSenhas não conferem!\n\n")


def login():
    """retorna o id do usuário logado"""
    email = input("Digite seu email:  ")
    senha = maskpass.askpass(prompt='Senha:',mask = "#")
    #senha = input("Digite sua senha:  ")
    users = read_csv("static/users.csv")
    wanted = users["senha"][users['email'] == email].to_list()
    if senha in wanted:
        print("Login efetuado!")
        return users.loc[users['email'] == email]['id_user'].values[0].tolist()

    else:
        print("\nUsuário e/ou senha errados!\n")
        return 0
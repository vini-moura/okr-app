from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=["POST","GET"])
def home():
    return render_template('monitorar.html')

@app.route("/atualizar", methods=["POST"])
def receive_data():
    setor = request.form["setor"]
    okr = request.form["okr"]
    kr = request.form["kr"]
    ppp = request.form["ppp"]
    v_atual = request.form["v_atual"]
    return f"<h1> setor {setor} |okr {okr}| kr {kr}| ppp {ppp}| v_atual {v_atual} </h1>"

@app.route('/atualizar', methods=["POST","GET"])
def atualizar():
    return render_template("atualizar.html")

@app.route('/monitorar', methods=["POST","GET"])
def monitorar():
    return render_template("monitorar.html")

@app.route('/cadastrar', methods=["POST","GET"])
def cadastrar():
    return render_template("cadastrar.html")


#@app.after_request  #permite requisição deo outros servidores
#def add_headers(response):
#    response.headers.add("Access-Control-Allow-Origin","*")
#    response.headers.add("Access-Control-Allow-Headers","Content-Type,Authorization")
#    return response


if __name__ == "__main__":
    app.run(debug=True)
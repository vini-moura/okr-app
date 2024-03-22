from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, DecimalField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from datetime import datetime
import requests

app = Flask(__name__)

class Base(DeclarativeBase):
    pass

app.config["SECRET_KEY"] = "Abaixo o capitalismo, viva Mark, Lenin e Mao!"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///okr.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)
bootstrap = Bootstrap5(app)

class Okrs(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_time: Mapped[int] = mapped_column(Integer, nullable=False)
    time: Mapped[str] = mapped_column(String(250), nullable=False)
    id_setor: Mapped[int] = mapped_column(Integer, nullable=False)
    setor: Mapped[str] = mapped_column(String(250), nullable=False)
    texto: Mapped[str] = mapped_column(String(250), nullable=False)
    responsavel: Mapped[str] = mapped_column(String(250), nullable=False)
    ano: Mapped[int] = mapped_column(Integer, nullable=False)
    ciclo: Mapped[int] = mapped_column(Integer, nullable=False)

class Krs(db.Model):
    id_kr: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_obj: Mapped[int] = mapped_column(Integer, nullable=False)
    texto: Mapped[str] = mapped_column(String(250), nullable=False)
    tipo: Mapped[str] = mapped_column(String(250), nullable=False)
    un_medida: Mapped[str] = mapped_column(String(250), nullable=False)
    inicial: Mapped[int] = mapped_column(Integer, nullable=False)
    valor_alterar: Mapped[float] = mapped_column(Float, nullable=False)
    meta: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(250), nullable=False)
    atual: Mapped[float] = mapped_column(Float, nullable=False)

class Usuarios(db.Model):
    id_user: Mapped[int] = mapped_column(Integer, primary_key=True)
    user: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    senha: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    time: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)

with app.app_context():
    db.create_all()
'''
new_kr = Krs(
    id_obj= 1,
    texto= "formar na ufms esse ano",
    tipo="aumentar",
    un_medida= "inteiro",
    inicial= 0,
    valor_alterar= 7,
    meta= 7,
    status= "novo",
    atual=1
)
with app.app_context():
    db.session.add(new_kr)
    db.session.commit()
'''

# class LoginForm(FlaskForm):
#    email = StringField('Email', validators=[DataRequired(), Email()])
#    password = PasswordField('Password', validators=[DataRequired()])
#    submit = SubmitField(label="Log in")

@app.route("/login", methods=["GET","POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if login_form.email.data == "admin@email.com" and login_form.password.data == "sirgas2000!":
            return render_template("success.html")
        else:
            return render_template("denied.html")
    return render_template('login.html', form=login_form)


@app.route('/', methods=["POST","GET"])
def home():
    now = datetime.now()
    current_year = now.year
    current_quarter = (now.month - 1) // 3 + 1  # Calcula o trimestre atual
    okr = db.session.execute(db.select(Okrs).where(Okrs.ano == current_year).where(Okrs.ciclo == current_quarter))
    #okr = Okrs.query.filter_by(ano=current_year, ciclo=current_quarter)
    okr = okr.scalars().all()

    ids_objs = [i.id for i in okr]
    krs = db.session.execute(db.select(Krs).where(Krs.id_obj.in_(ids_objs)))
    krs = krs.scalars().all()
    valores_atuais = [kr.atual for kr in krs]
    media_total = sum(valores_atuais) / len(valores_atuais)
    n = 1
    return render_template('monitorar.html', okr=okr, krs=krs, media_total=media_total)


@app.route("/atualizar", methods=["GET","POST"])
def atualizar():
    idp = request.args.get("idp")
    kr = db.session.execute(db.select(Krs).where(Krs.id_kr == idp)).scalar()
    return render_template("atualizar.html", kr=kr)

@app.route('/atualizar2', methods=["POST","GET"])
def atualizar2():
    return render_template("atualizar.html")

@app.route('/monitorar', methods=["POST","GET"])
def monitorar():
    return render_template("monitorar.html")

@app.route('/cadastrar', methods=["POST","GET"])
def cadastrar():
    return render_template("cadastrar.html")

@app.route('/perfil', methods=["POST","GET"])
def perfil():
    return render_template("cadastrar.html")

@app.route('/dashboard', methods=["POST","GET"])
def dashboard():
    return render_template("cadastrar.html")

@app.route('/contato', methods=["POST","GET"])
def contato():
    return render_template("cadastrar.html")

# @app.after_request  #permite requisição deo outros servidores
# def add_headers(response):
#    response.headers.add("Access-Control-Allow-Origin","*")
#    response.headers.add("Access-Control-Allow-Headers","Content-Type,Authorization")
#    return response


if __name__ == "__main__":
    app.run(debug=True)
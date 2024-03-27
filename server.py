from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap5
# from flask_wtf import FlaskForm
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
# from wtforms import StringField, IntegerField, FloatField, DecimalField, PasswordField, SubmitField
# from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from datetime import datetime
# import requests

app = Flask(__name__)
app.config["SECRET_KEY"] = "Abaixo o capitalismo, viva Mark, Lenin e Mao!"

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///okr.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)
bootstrap = Bootstrap5(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

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


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))

class Times(db.Model):
    id_setor: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_time: Mapped[str] = mapped_column(String(100))
    time: Mapped[str] = mapped_column(String(100))
    setor: Mapped[str] = mapped_column(String(100))


with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get('email')
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
        if user:
            flash("Email já cadastrado, faça o login")
            return redirect(url_for('login'))
        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=request.form.get('email'),
            password=hash_and_salted_password,
            name=request.form.get('name')
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        session['user_name'] = user.name
        session['user_id_time'] = user.id_time
        session['user_time'] = user.time
        return redirect(url_for("monitorar"))

    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("Email incorreto, tente novamente")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Senha incorreta, tente novamente')
            return redirect(url_for('login'))
        else:
            login_user(user)
            session['user_name'] = user.name
            session['user_id_time']= user.id_time
            session['user_time']= user.time
            return redirect(url_for('monitorar'))
    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/monitorar', methods=["POST","GET"])
def monitorar():
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
    name=session.get('user_name')
    time=session.get('user_time')
    return render_template('monitorar.html', okr=okr, krs=krs, media_total=media_total, user_name=name, user_time=time)


@app.route("/atualizar", methods=["GET","POST"])
def atualizar():
    if request.method == "POST":
        id_kr = request.form.get('kr_id')
        kr_texto = request.form.get('kr_texto')
        kr_meta = float(request.form.get('kr_meta'))
        ppp = request.form.get('ppp')
        novo_valor = float(request.form.get('novo_valor'))

        results = db.session.query(Krs).filter_by(id_kr=id_kr).first()
        results.texto = kr_texto
        results.meta = kr_meta
        results.atual = novo_valor
        db.session.commit()
        return redirect(url_for('monitorar'))
    name=session.get('user_name')
    time=session.get('user_time')
    idp = request.args.get("idp")
    kr = db.session.query(Krs).filter_by(id_kr=idp).first()
    return render_template("atualizar.html", kr=kr, user_name=name, user_time=time)


@app.route('/cadastrar', methods=["POST","GET"])
def cadastrar():
    if request.method=="POST":
        #id        id_time        time         id_setor   setor   texto  responsavel  ano  #ciclo
        id_time = session.get('user_time')
        time = session.get('time')
        id_setor= request.form.get('setor')
        result = db.session.execute(db.select(Times.setor).where(id_setor == id_setor))
        nome = result.scalar()
        print(f'nome é: {nome}')
        setor = nome
        print(f'setor é {setor}')
        texto = request.form.get('texto')
        responsavel = request.form.get('responsavel')
        ano = request.form.get('ano')
        ciclo = request.form.get('ciclo')
        novo = Okrs(
            id_time=id_time,
            time=time,
            id_setor=id_setor,
            setor=setor,
            texto = texto,
            responsavel = responsavel,
            ano = ano,
            ciclo = ciclo,
        )
        db.session.add(novo)
        db.session.commit()
        id_obj = novo.id
        n_krs = request.args.get('n_krs')
        return redirect(url_for('cadastrarkr', id_obj=id_obj, n_krs=n_krs))
    name = session.get('user_name')
    time = session.get('user_time')
    id_time = session.get('user_id_time')
    result = db.session.execute(db.select(Times).where(id_time==id_time))
    setores = result.scalars()

    return render_template("cadastrar.html", user_name=name, user_time=time, setores=setores)

@app.route('/cadastrarkr', methods=["POST", "GET"])
def cadastrarkr():
    if request.method == "POST":
        n_krs = int(request.form.get('n_krs'))
        for i in range(n_krs):
            id_obj = request.form.get(f'id_obj_{i}')
            texto = request.form.get(f'texto_{i}')
            tipo = request.form.get(f'tipo_{i}')
            uni_med = request.form.get(f'uni_med_{i}')
            valor_inicial = request.form.get(f'valor_inicial_{i}')
            meta = request.form.get(f'meta_{i}')
            status = "novo"
            atual = request.form.get(f'valor_inicial_{i}')
            print(texto)
            novo_kr = Krs(
                id_obj=id_obj,
                texto=texto,
                tipo=tipo,
                un_medida=uni_med,
                inicial=valor_inicial,
                valor_alterar=meta,
                meta=meta,
                status=status,
                atual=atual
            )
            db.session.add(novo_kr)
            db.session.commit()
        return redirect(url_for('monitorar'))

    n_krs = int(request.args.get('n_krs'))
    id_obj = request.args.get('id_obj')
    nome = session.get('user_name')
    time = session.get('user_time')
    return render_template("cadastrarkr.html", nome=nome, time=time, n_krs=n_krs, id_obj=id_obj)

@app.route('/perfil', methods=["POST","GET"])
def perfil():
    return render_template("cadastrar.html")

@app.route('/dashboard', methods=["POST","GET"])
def dashboard():
    return render_template("dashboard.html")

@app.route('/contato', methods=["POST","GET"])
def contato():
    return render_template("contato.html")

# @app.after_request  #permite requisição deo outros servidores
# def add_headers(response):
#    response.headers.add("Access-Control-Allow-Origin","*")
#    response.headers.add("Access-Control-Allow-Headers","Content-Type,Authorization")
#    return response


if __name__ == "__main__":
    app.run(debug=True)
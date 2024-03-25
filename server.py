from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from wtforms import StringField, IntegerField, FloatField, DecimalField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from datetime import datetime
import requests

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

        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=request.form.get('email'),
            password=hash_and_salted_password,
            name=request.form.get('name'),
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
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
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('secrets'))

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
import os
from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormRegister, FormPost
from fakepinterest.models import User, Post
from werkzeug.utils import secure_filename


@app.route("/login", methods=["GET", "POST"])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        user = User.query.filter_by(email=form_login.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form_login.password.data):
            login_user(user)
            return redirect(url_for("perfil", user_id=user.id))
    return render_template("login.html", form=form_login)


@app.route("/register", methods=["GET", "POST"])
def register():
    form_register = FormRegister()
    if form_register.validate_on_submit():
        password = bcrypt.generate_password_hash(form_register.password.data).decode("utf-8")
        user = User(username=form_register.username.data, email=form_register.email.data, password=password)
        
        database.session.add(user)
        database.session.commit()
        login_user(user, remember=True)
        return redirect(url_for("perfil", user_id=user.id))
    return render_template("register.html", form=form_register)


@app.route("/")
def homepage():
    return redirect(url_for("login"))


@app.route("/perfil/<user_id>", methods=["GET", "POST"])
@login_required
def perfil(user_id):
    if int(user_id) == int(current_user.id):
        form_post = FormPost()
        if form_post.validate_on_submit():
            file = form_post.photo.data
            filename = secure_filename(file.filename)
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], filename)
            file.save(path)
            post = Post(image=filename, user_id=current_user.id)
            database.session.add(post)
            database.session.commit()
            return redirect(url_for("perfil", user_id=current_user.id))
        return render_template("perfil.html", user=current_user, form=form_post)
    else:
        user = User.query.get(int(user_id))
        return render_template("perfil.html", user=user, form=None)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/feed")
@login_required
def feed():
    posts = Post.query.order_by(Post.publish_date.desc()).all()
    return render_template("feed.html", posts=posts)
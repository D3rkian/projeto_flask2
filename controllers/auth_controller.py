# 1. Importe tudo que as rotas precisam
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db, Usuario 


auth_bp = Blueprint(
    'auth', __name__,
    template_folder='../templates' 
)



@auth_bp.route('/')
def index():
    return render_template('login_registro.html')

@auth_bp.route('/registrar', methods=['POST'])
def registrar():
    
    if Usuario.query.filter_by(username=request.form.get('username')).first():
        flash('Este nome de usuário já existe.', 'error')
        return redirect(url_for('auth.index'))

    novo_usuario = Usuario(username=request.form.get('username'))
    novo_usuario.set_password(request.form.get('password'))
    db.session.add(novo_usuario)
    db.session.commit()

    flash('Usuário criado! Faça o login.', 'success')
    return redirect(url_for('auth.index'))

@auth_bp.route('/login', methods=['POST'])
def login():
    
    username = request.form.get('username')
    password = request.form.get('password')
    user = Usuario.query.filter_by(username=username).first()

    if user and user.check_password(password):
        login_user(user)
        
        return redirect(url_for('auth.area_protegida'))
    else:
        flash('Usuário ou senha inválidos.', 'error')
        return redirect(url_for('auth.index'))

@auth_bp.route('/logout')
@login_required
def logout():
    
    logout_user()
    flash('Você foi desconectado.', 'success')
    return redirect(url_for('auth.index'))

@auth_bp.route('/protegida')
@login_required
def area_protegida():
    
    return render_template('index.html')
from flask import render_template, request, url_for, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.model import Usuario
from app import app, db

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')

    usuario = Usuario.query.filter_by(email_user=email).first()

    if usuario and check_password_hash(usuario.senha_user, senha):
        flash('Login realizado com sucesso!', 'success')
        return render_template('home.html', nome_usuario=usuario.nome_user)
    else:
        flash('E-mail ou senha incorretos', 'error')
        return render_template('index.html', error_message='Login falhou. Verifique suas credenciais.')
    

    
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        # Validações básicas
        if not all([nome, email, senha]):
            flash('Por favor, preencha todos os campos', 'error')
            return redirect(url_for('cadastro'))

        # Verifica se usuário já existe
        usuario_existente = Usuario.query.filter_by(email_user=email).first()
        if usuario_existente:
            flash('E-mail já cadastrado', 'error')
            return redirect(url_for('cadastro'))

        try:
            novo_usuario = Usuario(
                nome_user=nome,
                email_user=email,
                senha_user=generate_password_hash(senha, method='pbkdf2:sha256')
            )
            
            db.session.add(novo_usuario)
            db.session.commit()
            
            flash('Cadastro realizado com sucesso! Faça login', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Erro no cadastro: {str(e)}')
            flash('Ocorreu um erro durante o cadastro. Por favor, tente novamente.', 'error')
            return redirect(url_for('cadastro'))

    return render_template('cadastro.html')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)

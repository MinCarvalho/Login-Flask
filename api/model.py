from api.index import db

class Usuario(db.Model):
    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_user = db.Column(db.String(150))
    email_user = db.Column(db.String(150), unique=True)
    senha_user = db.Column(db.String(150))



  
from . import db
from passlib.hash import sha256_crypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True)
    password = db.Column(db.String(500))
    email = db.Column(db.String(50))
    settings = db.Column(db.String(32500))

    def authentication(self, input_password):
    	return sha256_crypt.verify(input_password, self.password)

    def set_password(self, input_password):
    	self.password = sha256_crypt.encrypt((str(input_password)))

    def __repr__(self):
        return '<User %r>' % (self.username)


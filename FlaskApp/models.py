from . import db
from passlib.hash import sha256_crypt


# class Role(db.Model):
#     __tablename__= 'roles'
#     users = db.relationship('User', backref='role')
#     name = db.Column(db.String(64), unique = True)
#     id = db.Column(db.Integer, primary_key= True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True)
    password = db.Column(db.String(500))
    email = db.Column(db.String(50), unique = True)
    #role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def is_active(self):
        return True

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    @property
    def is_authenticated(self):
            return True

    @property
    def is_anonymous(self):
            return False

    def authentication(self, input_password):
    	return sha256_crypt.verify(input_password, self.password)

    def set_password(self, input_password):
    	self.password = sha256_crypt.encrypt((str(input_password)))

    def __repr__(self):
        return '<User %r>' % (self.username)

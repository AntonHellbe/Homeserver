from . import db
from passlib.hash import sha256_crypt
from datetime import datetime


# class Role(db.Model):
#     __tablename__= 'roles'
#     users = db.relationship('User', backref='role')
#     name = db.Column(db.String(64), unique = True)
#     id = db.Column(db.Integer, primary_key= True)

class Project(db.Model):
    __tablename__='projects'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique = True, index = True)
    tags = db.Column(db.String(64))
    description = db.Column(db.Text)
    date = db.Column(db.DateTime)
    links = db.Column(db.String(512), nullable = True)
    image_filename = db.Column(db.String(128), default = None, nullable = True)
    image_url = db.Column(db.String(128), default = None, nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def generate_fake(count=20):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = Project(name = forgery_py.lorem_ipsum.word(),
                        tags = forgery_py.lorem_ipsum.word() + "," + forgery_py.lorem_ipsum.word(),
                        description = forgery_py.lorem_ipsum.sentence(),
                        date = forgery_py.date.date(True),
                        links = forgery_py.lorem_ipsum.word(),
                        user_id = u.id)

            db.session.add(p)
            try:
                db.session.commit()
            except:
                db.session.rollback()



    def __repr__(self):
        return '<Project %r>' % self.name

class User(db.Model):
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, index = True)
    password = db.Column(db.String(500))
    email = db.Column(db.String(50), unique = True)
    last_logged_in = db.Column(db.DateTime(), default=datetime.utcnow)
    projects = db.relationship('Project', backref='author', lazy='dynamic')

    @property
    def is_active(self):
        return True

    # @property
    # def password(self):
    #    raise AttributeError('Password is not a readable attritbute')

    def ping(self):
        self.last_logged_in = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

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
    	self.password = sha256_crypt.encrypt((input_password))

    def generate_fake(count = 20):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User(username = forgery_py.internet.user_name(True),
                     email = forgery_py.internet.email_address(),
                     last_logged_in = forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except:
                db.session.rollback()

    def __repr__(self):
        return '<User %r>' % (self.username)

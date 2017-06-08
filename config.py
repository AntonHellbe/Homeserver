import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:////sqlite/test.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
#SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'super-mega-secretkey123456789'

SECRET_KEY = 'abc123456789fghjklmnopqwet1231543rmkadmsa'
SECURITY_REGISTERABLE = True

#print(basedir)
#print(SQLALCHEMY_DATABASE_URI)
#print(SQLALCHEMY_TRACK_MODIFICATIONS)
#print(SQLALCHEMY_MIGRATE_REPO)

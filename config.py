import secrets
import urllib.parse as parse

class Config:
    SECRET_KEY = secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:notlb@localhost:3306/sigp'.format(parse.quote(""))
    SESSION_COOKIE_HTTPONLY=False
    SESSION_COOKIE_SAMESITE="Lax"
import secrets
import urllib.parse as parse
import os

class Config:
    SECRET_KEY = secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:notlb@localhost:3306/sigp'.format(parse.quote(""))
    SESSION_COOKIE_HTTPONLY=False
    SESSION_COOKIE_SAMESITE="Lax"
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    UPLOAD_DOCUMENTOS = os.path.join(BASE_DIR, "uploads", "documentos")
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20 MB
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'jpg', 'jpeg', 'png'}

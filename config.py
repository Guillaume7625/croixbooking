import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'votre-clé-secrète'  # Remplacez par une vraie clé secrète
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = 'votre-clé-api-openai'  # Remplacez par votre vraie clé API OpenAI
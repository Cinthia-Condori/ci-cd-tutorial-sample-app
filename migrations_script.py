from app import create_app, db, migrate

app = create_app()

# Esto es necesario para registrar 'flask db' correctamente
from flask_migrate import MigrateCommand
from flask.cli import with_appcontext

# Solo importa tus modelos aquí
from app import models

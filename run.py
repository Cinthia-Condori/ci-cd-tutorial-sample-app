from app import create_app, db

# Creamos la app Flask
app = create_app()

# Creamos las tablas de la base de datos dentro del contexto de la app
with app.app_context():
    db.create_all()
    print("Base de datos creada correctamente.")

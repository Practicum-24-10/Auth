from src.main import app
from src.db.postgres_db import db, init_db
from src.models import *

# Подготоваливаем контекст и создаём таблицы
init_db(app)
app.app_context().push()
db.create_all()

# Insert-запросы
admin = User(login='lfdsdsdsdsoeel', password='password')
role = Role(name='addmin')
perm = Permission(permission='VeIP')
role.permissions.append(perm)
admin.roles.append(role)
db.session.add(admin)
db.session.commit()

# Select-запросы
User.query.all()
User.query.filter_by(login='addmin').first()

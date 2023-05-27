from sqlalchemy.dialects.postgresql import UUID

from src.db.postgres_db import db
from src.models.mixin import Mixin

# UsersRole = db.Table('users_roles',
#                      db.Column('user_id', UUID(as_uuid=True),
#                                db.ForeignKey('users.id', ondelete='CASCADE'),
#                                primary_key=False),
#                      db.Column('role_id', UUID(as_uuid=True),
#                                db.ForeignKey('roles.id', ondelete='CASCADE'),
#                                primary_key=False))
# class UsersRole:
#     __tablename__ = 'roles_permissions'


class UsersRole(db.Model):
    __tablename__ = "users_roles"

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), primary_key=True)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey("roles.id"), primary_key=True)


class Role(Mixin):
    __tablename__ = "roles"

    name = db.Column(db.String, unique=True, nullable=False)
    users = db.relationship(
        "User", secondary="users_roles", overlaps="roles,users_relation"
    )
    permissions = db.relationship(
        "Permission",
        secondary="roles_permissions",
        overlaps="permissions,roles_relation",
    )

    # permissions_relation = db.relationship('Permission',
    #                                        secondary=RolesPermissions,
    #                                        backref='roles')

    def __repr__(self):
        return f"<Role {self.name}>"


# class UsersRole(db.Model):
#     __tablename__ = 'users_roles'
#
#     user_id = db.Column(db.ForeignKey('users.id', ondelete='CASCADE'),
#                         nullable=False, primary_key=False)
#     role_id = db.Column(db.ForeignKey('roles.id', ondelete='CASCADE'),
#                         nullable=False, primary_key=False)
#
# ```
#
#
# class Permission(Base):
#     __tablename__ = 'permissions'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#
#     roles = relationship('Role', secondary='roles_permissions',
#                          overlaps="permissions,roles_relation")
#
#
# class Role(Base):
#     __tablename__ = 'roles'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#
#     permissions = relationship('Permission', secondary='roles_permissions')
#
#
# class RolesPermissions(Base):
#     __tablename__ = 'roles_permissions'
#
#     permission_id = Column(Integer, ForeignKey('permissions.id'),
#                            primary_key=True)
#     role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)
#     grant = Column(Boolean, nullable=False)
#
#
# ```

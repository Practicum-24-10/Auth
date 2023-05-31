from sqlalchemy.dialects.postgresql import UUID

from src.db.postgres_db import db
from src.models.mixin import Mixin


# RolesPermissions = db.Table('roles_permissions',
#                             db.Column('user_id', UUID(as_uuid=True),
#                                       db.ForeignKey('roles.id',
#                                                     ondelete='CASCADE'),
#                                       primary_key=False),
#                             db.Column('role_id', UUID(as_uuid=True),
#                                       db.ForeignKey('permissions.id',
#                                                     ondelete='CASCADE'),
#                                       primary_key=False))
class RolesPermissions(db.Model):
    __tablename__ = "roles_permissions"

    permission_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("permissions.id"), primary_key=True
    )
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey("roles.id"), primary_key=True)


class Permission(Mixin):
    __tablename__ = "permissions"

    permission = db.Column(db.String, unique=True, nullable=False)
    roles = db.relationship(
        "Role", secondary="roles_permissions", overlaps="permissions,roles_relation"
    )

    def __repr__(self):
        return f"<Permission {self.permission}>"



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

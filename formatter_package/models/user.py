from enum import Enum


class Role(str, Enum):
    UPLOADER = "uploader"
    APPROVER = "approver"


class User:
    def __init__(self, username: str, password: str, role: Role):
        if not isinstance(role, Role):
            raise ValueError(f"role must be an instance of Role Enum, got {role}")
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            "username": self.username,
            "role": self.role.value
        }

    def __repr__(self):
        return f"User(username={self.username!r}, role={self.role.value!r})"

    def has_permission(self, action: str) -> bool:
        permissions = {
            Role.UPLOADER: {"upload"},
            Role.APPROVER: {"approve", "upload"},
        }
        return action in permissions.get(self.role, set())

import os

from cryptography.fernet import Fernet
from sqlalchemy import String
from sqlalchemy.types import TypeDecorator

from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()

_key = os.getenv("FERNET_KEY")

if not _key:
    raise RuntimeError("FERNET_KEY is not set")

_fernet = Fernet(_key.encode())


class EncryptedString(TypeDecorator):
    """Transparently encrypts/decrypts a string column at rest."""

    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        # Python value -> DB value (on INSERT/UPDATE)
        if value is None:
            return None
        return _fernet.encrypt(value.encode("utf-8")).decode("utf-8")

    def process_result_value(self, value, dialect):
        # DB value -> Python value (on SELECT)
        if value is None:
            return None
        return _fernet.decrypt(value.encode("utf-8")).decode("utf-8")
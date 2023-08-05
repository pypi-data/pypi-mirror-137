"""
    :copyright: 2021 Inmanta
    :contact: code@inmanta.com

    This file contains all functionality related to discovering modules from remote git provides.

"""

import os
from typing import Dict, Optional

from pydantic import BaseModel


class Credential(BaseModel):

    username: Optional[str]
    password: str


class CredentialStore:
    """
    A uniform way of passing credentials through the code.
    """

    def __init__(self) -> None:
        self.credentials: Dict[str, Credential] = {}

    def get_credentials_for(self, name: str) -> Optional[Credential]:
        """return username/password for a specific source"""
        return self.credentials.get(name, None)

    def set_credentials_for(
        self, name: str, username: Optional[str], password: str
    ) -> None:
        self.credentials[name] = Credential(username=username, password=password)


class FromEnvCredentialStore(CredentialStore):
    """
    A CredentialStore that will attempt to find credentials that are absent in environment variables.
    """

    def get_credentials_for(self, name: str) -> Optional[Credential]:
        out = super().get_credentials_for(name)
        if out is not None:
            return out
        if f"{name.upper()}_TOKEN" in os.environ:
            token = os.environ[f"{name.upper()}_TOKEN"]
            username = os.environ.get(f"{name.upper()}_USERNAME", None)
            return Credential(username=username, password=token)
        return None

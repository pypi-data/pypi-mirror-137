"""
    :copyright: 2021 Inmanta
    :contact: code@inmanta.com

    This file contains all functionality related to discovering modules from remote git provides.

"""
import enum
import os
from typing import Dict, Optional

from pydantic import BaseModel


class CredentialName(enum.Enum):
    """
    The names of the credentials that can be stored in a CredentialStore.
    This call serves two purposes:
      1) Prevent typos when providing the name of a credential to the CredentialStore.
      2) Provide a docstring regarding the meaning of each credential commonly used.
    """

    GITHUB = "github"
    """Token to clone GitHub repositories"""
    GITLAB = "gitlab"
    """Token to clone GitLab repositories"""
    CLOUDSMITH_API_KEY = "cloudsmith_api_key"
    """Token to download/publish packages to cloudsmith"""
    PGP_PASS = "pgp_pass"
    """Passphrase for the key used to sign the Python packages published to PyPi."""


class Credential(BaseModel):

    username: Optional[str]
    password: str


class CredentialStore:
    """
    A uniform way of passing credentials through the code.
    """

    def __init__(self) -> None:
        self.credentials: Dict[CredentialName, Credential] = {}

    def get_credentials_for(
        self, name: CredentialName, allow_unset: bool = True
    ) -> Optional[Credential]:
        """return username/password for a specific source"""
        result = self.credentials.get(name, None)
        if result is None and not allow_unset:
            raise Exception(
                f"Credential {name.value} is not present in the credential store."
            )
        return result

    def set_credentials_for(
        self, name: CredentialName, username: Optional[str], password: str
    ) -> None:
        self.credentials[name] = Credential(username=username, password=password)


class FromEnvCredentialStore(CredentialStore):
    """
    A CredentialStore that will attempt to find credentials that are absent in environment variables.
    """

    def get_credentials_for(
        self, name: CredentialName, allow_unset: bool = True
    ) -> Optional[Credential]:
        out = super().get_credentials_for(name, allow_unset=True)
        if out is not None:
            return out
        env_var_token = f"{name.value.upper()}_TOKEN"
        env_var_username = f"{name.value.upper()}_USERNAME"
        if env_var_token in os.environ:
            token = os.environ[env_var_token]
            username = os.environ.get(env_var_username, None)
            return Credential(username=username, password=token)
        if not allow_unset:
            raise Exception(
                f"Credential {name.value} is not present in the credential store."
            )
        return None

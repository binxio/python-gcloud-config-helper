import json
import logging
import shutil
import subprocess
from datetime import datetime
from typing import Dict, Optional

from dateutil.parser import isoparse
from google.auth.credentials import Credentials, CredentialsWithQuotaProject
from pytz import utc


class GCloudCredentials(CredentialsWithQuotaProject):
    """
    Google gcloud configuration credentials.
    """
    def __init__(self, name: str = ""):
        super(GCloudCredentials, self).__init__()
        self.config: Dict = {}
        self._name: str = name
        self.token: Optional[str] = None
        self.expiry: Optional[datetime] = None

        self.refresh(None)

    def with_quota_project(self, quota_project_id):
        result = type(self)(self._name)
        result._quota_project_id = quota_project_id
        return result

    @property
    def name(self) -> str:
        """
        of the active gcloud configuration.
        """
        return self.config.get("configuration", {}).get(
            "active_configuration", self._name
        )

    def load(self):
        """
        executes the gcloud config config-helper for the configuration with `self._name` and stores the resulting
        dictionary in `self.config`.
        """
        gcloud_absolute_path = shutil.which('gcloud')
        process = subprocess.Popen(
            [
                gcloud_absolute_path,
                "config",
                "config-helper",
                "--configuration",
                self._name,
                "--format",
                "json",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        out, err = process.communicate()
        if process.returncode != 0:
            logging.fatal(
                "gcloud config config-helper exited with %d, %s",
                process.returncode,
                err,
            )
            exit(1)

        self.config = json.loads(out)

    @property
    def properties(self) -> Dict:
        """
        the gcloud configuration properties
        """
        return self.config.get("configuration", {}).get("properties", {})

    @property
    def credential(self) -> Dict:
        """
        the current credential
        """
        return self.config.get("credential", {})

    @property
    def project(self) -> Optional[str]:
        """ "
        the configured project
        """
        return self.properties.get("core", {}).get("project")

    @property
    def token_expiry(self) -> Optional[datetime]:
        """
        the expiration date of the current credential
        """
        exp = self.credential.get("token_expiry")
        return isoparse(exp).astimezone(utc).replace(tzinfo=None) if exp else None

    @property
    def access_token(self) -> Optional[str]:
        """
        the current access token
        """
        return self.credential.get("access_token")

    def refresh(self, request):
        """
        refreshes the credentials.
        """
        self.load()
        self.token = self.access_token
        self.expiry = self.token_expiry


def on_path() -> bool:
    """
    returns True if gcloud is on your path, otherwise False
    """
    return shutil.which("gcloud") is not None


def default() -> (CredentialsWithQuotaProject, Optional[str]):
    """
    returns the current credentials and configured project in the
    gcloud active configuration
    """
    c = GCloudCredentials()
    return c, c.project

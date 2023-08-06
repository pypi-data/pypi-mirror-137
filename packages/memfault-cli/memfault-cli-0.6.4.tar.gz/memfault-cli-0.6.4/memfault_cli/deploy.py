import logging
from typing import Tuple, Union

import requests
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from .authenticator import Authenticator
from .context import MemfaultCliClickContext

LOG = logging.getLogger(__name__)


class Deployer:
    def __init__(self, *, ctx: MemfaultCliClickContext, authenticator: Authenticator):
        self.ctx: MemfaultCliClickContext = ctx
        self.authenticator: Authenticator = authenticator
        self.session = self._create_requests_session()

    @staticmethod
    def _create_requests_session() -> Session:
        retry_strategy = Retry(
            total=5,
            backoff_factor=2,  # Sleep for 2s, 4s, 8s, 16s, 32s, Stop
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "POST", "PUT"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = requests.Session()
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    @property
    def base_url(self) -> str:
        return self.ctx.api_url

    def _api_base_url(self) -> str:
        return f"{self.base_url}/api/v0"

    def _projects_base_url(self) -> str:
        return f"{self.base_url}/api/v0/organizations/{self.ctx.org}/projects/{self.ctx.project}"

    @property
    def deployment_url(self) -> str:
        """
        The upload URL for a 'prepared upload' for the configured authentication method.
        """
        return f"{self._projects_base_url()}/deployments"

    def deploy(
        self, *, release_version: Union[str, Tuple[str, str]], cohort: str, rollout_percent: int
    ) -> None:
        json_d = {
            "type": "normal" if rollout_percent == 100 else "staged_rollout",
            "release": release_version,
            "rollout_percent": rollout_percent,
            "cohort": cohort,
        }

        response = self.session.post(
            self.deployment_url, json=json_d, **self.authenticator.requests_auth_params()
        )
        if response.status_code >= 400:
            raise Exception(
                f"Request failed with HTTP status {response.status_code}\nResponse body:\n{response.content.decode()}"
            )
        LOG.info("Release %s successfully deployed to Cohort %s", release_version, cohort)

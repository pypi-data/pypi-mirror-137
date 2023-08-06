import logging
import os
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, AnyStr, Dict, List, Optional
from urllib.parse import urljoin

import jwt
import requests

from ruleau.decorators import api_request
from ruleau.exceptions import CaseAPIException, RuleAPIException
from ruleau.process import Process

if TYPE_CHECKING:
    from ruleau.structures import ExecutionResult

logger = logging.getLogger(__name__)


class ApiAdapter:
    base_url: AnyStr
    base_path: AnyStr
    username: Optional[AnyStr]
    password: Optional[AnyStr]

    def __init__(
        self,
        base_url: AnyStr,
        username: Optional[AnyStr] = None,
        password: Optional[AnyStr] = None,
    ):
        """
        :param base_url: Base URL of the ruleau API
        :param username: (Optional) Users username
        :param password: (Optional) Users password
        """
        self.base_url = base_url
        self.base_path = "/api/v1/"

        self.username = os.getenv("RULEAU_USERNAME", username)
        self.password = os.getenv("RULEAU_PASSWORD", password)
        if not self.username or not self.password:
            raise ValueError("Username or Password not supplied")

        self.access_token = None
        self.refresh_token = None
        self.access_token_expiry = None
        self.session = None
        self._fetch_JWT_token()

    def _fetch_JWT_token(self):
        """
        Fetches the JWT token for the username and password provided
        """
        login_response = requests.post(
            urljoin(self.base_url, f"{self.base_path}token/"),
            data={"username": self.username, "password": self.password},
        )
        if login_response.status_code != 200:
            raise requests.exceptions.RequestException(login_response.json())

        body = login_response.json()
        self.access_token = body["access"]
        self.refresh_token = body["refresh"]
        self._set_access_token_expiry(body)

    def _set_access_token_expiry(self, body):
        """
        Decodes the expiry time for the access token
        """
        access_payload = jwt.decode(body["access"], options={"verify_signature": False})
        self.access_token_expiry = datetime.fromtimestamp(int(access_payload["exp"]))

    def _refresh_access_token(self):
        """
        Gets a new access token using the refresh token
        """

        refresh_response = requests.post(
            urljoin(self.base_url, f"{self.base_path}token/refresh/"),
            data={
                "refresh": self.refresh_token,
            },
        )
        if refresh_response.status_code != 200:
            raise requests.exceptions.RequestException(refresh_response.json())

        body = refresh_response.json()
        self.access_token = body["access"]
        self._set_access_token_expiry(body)

    def _check_access_token_is_active(self):
        """
        Checks to see if the access token is close to expiring (within 5 seconds)
        or has expired
        """
        time_now = datetime.now()
        if time_now > (self.access_token_expiry - timedelta(seconds=5)):
            self._refresh_access_token()

    def _create_requests_session(self):
        self.session = requests.session()
        self.session.headers.update({"Authorization": f"Bearer {self.access_token}"})

    @api_request
    def sync_case(self, case_id: AnyStr, process_id: AnyStr, payload: Dict) -> Dict:
        """
        Synchronise case with API
        :param case_id: The ID of the case being executed
        :param process_id: The ID of the process
        :param payload: Case payload to execute on
        :return:
        """

        response = self.session.get(
            urljoin(
                self.base_url,
                f"{self.base_path}processes/{process_id}/cases/{case_id}",
            ),
        )

        if response.status_code == 200:
            response = self.session.patch(
                urljoin(
                    self.base_url,
                    f"{self.base_path}processes/{process_id}/cases/{case_id}",
                ),
                json={
                    "id": case_id,
                    "payload": payload,
                    "status": "OPEN",
                },
            )
            if response.status_code != 200:
                raise CaseAPIException(
                    activity="update", case_id=case_id, response=response
                )

        elif response.status_code == 404:
            response = self.session.post(
                urljoin(self.base_url, f"{self.base_path}processes/{process_id}/cases"),
                headers={"Authorization": f"Bearer {self.access_token}"},
                json={
                    "id": case_id,
                    "payload": payload,
                    "process": process_id,
                    "status": "OPEN",
                },
            )
            if response.status_code != 201:
                raise CaseAPIException(
                    activity="create", case_id=case_id, response=response
                )

        else:
            raise CaseAPIException(activity="check", case_id=case_id, response=response)

        return response.json()

    @api_request
    def sync_process(self, process: Process):

        response = self.session.post(
            urljoin(self.base_url, f"{self.base_path}processes"),
            headers={"Authorization": f"Bearer {self.access_token}"},
            json=process.parse(),
        )

        if response.status_code != 201:
            raise RuleAPIException(
                activity="save", process_id=process.id, response=response
            )

        return response.json()

    @api_request
    def sync_results(
        self,
        process: "Process",
        case_id: AnyStr,
    ):
        payload = [
            {
                "rule": rule.id,
                "result": rule.execution_result.result,
                "payloads": rule.execution_result.payload.accessed
                if rule.execution_result.payload
                else None,
                "override": rule.execution_result.override,
                "original_result": rule.execution_result.original_result,
                "skipped": rule.execution_result.skipped,
            }
            for rule in process.rules
            if rule.execution_result
        ]
        response = self.session.post(
            urljoin(
                self.base_url,
                f"{self.base_path}processes/{process.id}/cases/" f"{case_id}/results",
            ),
            headers={"Authorization": f"Bearer {self.access_token}"},
            json=payload,
        )
        if response.status_code > 299:
            raise RuleAPIException(
                activity="store rule result for",
                process_id=process.id,
                response=response,
            )
        return None

    @api_request
    def fetch_override(
        self, case_id: AnyStr, process_id: AnyStr, rule_id: AnyStr
    ) -> Optional[Dict[AnyStr, Any]]:
        """
        Fetch rule overrides
        :param case_id: client ID that identifies a previously established case
        :param process_id: The ID of the process that the case is being run against
        :param rule_id: The ID of the Rule to fetch overrides for
        :return: a ruleau overrides Optional[Dict[AnyStr, Any]]
        """

        response = self.session.get(
            urljoin(
                self.base_url,
                f"{self.base_path}processes/{process_id}/"
                f"cases/{case_id}/overrides/search",
            ),
            headers={"Authorization": f"Bearer {self.access_token}"},
            params={"rule_id": rule_id},
        )
        if response.status_code != 200:
            return {}
        return response.json()

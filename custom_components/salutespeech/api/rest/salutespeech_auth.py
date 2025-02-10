"""SaluteSpeech authorization helper."""

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import uuid
from datetime import datetime, timedelta
from typing import Optional

from aiohttp import ClientSession
from homeassistant.helpers.aiohttp_client import async_get_clientsession


class SaluteSpeechAuth:
    def __init__(self, hass, auth_key: str, scope: str = "SALUTE_SPEECH_PERS") -> None:
        """SaluteSpeech authorization helper."""
        self._session: ClientSession = async_get_clientsession(hass)
        self._auth_key: str = auth_key
        self._scope: str = scope
        self._token_url: str = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        self._access_token: Optional[str] = None
        self._expires_at: Optional[datetime] = None

    def _generate_rquid(self) -> str:
        """Get unique request ID."""
        return str(uuid.uuid4())

    async def get_access_token(self) -> Optional[str]:
        """Return the access token. If it exists and valid, return it. Otherwise, fetch a new one."""
        if self._access_token and datetime.now() < self._expires_at:
            return self._access_token

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": self._generate_rquid(),
            "Authorization": f"Basic {self._auth_key}",
        }

        payload = {"scope": self._scope}

        try:
            async with self._session.post(
                self._token_url, headers=headers, data=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(
                        f"Failed to get access token: {response.status} {error_text}"
                    )

                data = await response.json()
                self._access_token = data.get("access_token")
                expires_in = 1800  # 30 minutes
                self._expires_at = datetime.now() + timedelta(seconds=expires_in - 59)
                return self._access_token

        except Exception as e:
            raise Exception(f"Error during token request: {e}")

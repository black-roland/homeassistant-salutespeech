"""Config flow for SaluteSpeech integration."""

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import CONF_AUTH_KEY, CONF_VERIFY_SSL, DOMAIN

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_AUTH_KEY): str,
        vol.Required(CONF_VERIFY_SSL): bool,
    }
)


class SaluteSpeechConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SaluteSpeech."""

    VERSION = 1
    MINOR_VERSION = 0

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""

        if user_input is not None:
            # TODO: Validate input
            return self.async_create_entry(
                title="SaluteSpeech",
                data=user_input,
            )

        advanced_schema = vol.Schema(
            {
                vol.Required(CONF_VERIFY_SSL, default=False): bool,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_AUTH_KEY): str,
                    **(advanced_schema.schema if self.show_advanced_options else {}),
                }
            ),
        )

"""The SaluteSpeech integration."""

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from custom_components.salutespeech.const import (
    CONF_AUTH_KEY,
    CONF_USE_BUNDLED_ROOT_CERTIFICATES,
    DATA_AUTH_HELPER,
    DATA_ROOT_CERTIFICATES,
)

from .api.rest.salutespeech_auth import SaluteSpeechAuth

PLATFORMS = [Platform.STT, Platform.TTS]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a config entry."""

    def read_root_certificates():
        file_name = os.path.join(
            os.path.dirname(__file__),
            "api",
            "certs",
            "russian_trusted_root_ca.cer",
        )
        return open(file_name, "rb").read()

    root_certificates = (
        await hass.async_add_executor_job(read_root_certificates)
        if entry.data.get(CONF_USE_BUNDLED_ROOT_CERTIFICATES, True)
        else None
    )

    entry.runtime_data = {}
    entry.runtime_data[DATA_ROOT_CERTIFICATES] = root_certificates
    entry.runtime_data[DATA_AUTH_HELPER] = SaluteSpeechAuth(
        hass, entry.data[CONF_AUTH_KEY], root_certificates
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

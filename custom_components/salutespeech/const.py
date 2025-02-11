"""Constants for the SaluteSpeech integration."""

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging

DOMAIN = "salutespeech"
LOGGER = logging.getLogger(__package__)

CONF_AUTH_KEY = "auth_key"
CONF_VERIFY_SSL = "verify_ssl"

STT_LANGUAGES = ["ru-RU", "en-US", "kk-KZ"]

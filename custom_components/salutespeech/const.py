"""Constants for the SaluteSpeech integration."""

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging

from .api.grpc import synthesis_pb2

DOMAIN = "salutespeech"
LOGGER = logging.getLogger(__package__)

CONF_AUTH_KEY = "auth_key"
CONF_VERIFY_SSL = "verify_ssl"

DATA_AUTH_HELPER = "auth_helper"
DATA_ROOT_CERTIFICATES = "root_certificates"

SUPPORTED_LANGUAGES = ["ru-RU", "en-US", "kk-KZ"]

TTS_VOICES = {
    "en-US": [
        ("Kira", "Kin"),
    ],
    "kk-KZ": [
        ("Наталья", "Nec"),
        ("Борис", "Bys"),
        ("Марфа", "May"),
        ("Тарас", "Tur"),
        ("Александра", "Ost"),
        ("Сергей", "Pon"),
    ],
    "ru-RU": [
        ("Наталья", "Nec"),
        ("Борис", "Bys"),
        ("Марфа", "May"),
        ("Тарас", "Tur"),
        ("Александра", "Ost"),
        ("Сергей", "Pon"),
    ],
}

TTS_OUTPUT_CONTAINERS = {
    "wav": synthesis_pb2.SynthesisRequest.WAV,
    "opus": synthesis_pb2.SynthesisRequest.OPUS,
}

DEFAULT_LANG = "ru-RU"
DEFAULT_VOICE = "Nec"
DEFAULT_OUTPUT_CONTAINER = "wav"

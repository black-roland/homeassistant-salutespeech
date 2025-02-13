"""Support for the SaluteSpeech text-to-speech service."""

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import io
from typing import Any

import grpc
from grpc import aio
from homeassistant.components.tts import (
    ATTR_AUDIO_OUTPUT,
    ATTR_VOICE,
    TextToSpeechEntity,
    TtsAudioType,
    Voice,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api.grpc import synthesis_pb2, synthesis_pb2_grpc
from .const import (
    DATA_AUTH_HELPER,
    DATA_ROOT_CERTIFICATES,
    DEFAULT_LANG,
    DEFAULT_OUTPUT_CONTAINER,
    DEFAULT_VOICE,
    DOMAIN,
    LOGGER,
    SUPPORTED_LANGUAGES,
    TTS_OUTPUT_CONTAINERS,
    TTS_VOICES,
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SaluteSpeech text-to-speech."""
    entities: list[TextToSpeechEntity] = [SaluteSpeechTTSEntity(config_entry)]
    async_add_entities(entities)


class SaluteSpeechTTSEntity(TextToSpeechEntity):
    """The SaluteSpeech TTS entity."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize the entity."""
        self._attr_unique_id = config_entry.entry_id
        self._attr_name = config_entry.title
        self._attr_device_info = dr.DeviceInfo(
            identifiers={(DOMAIN, config_entry.entry_id)},
            manufacturer="Sber",
            model="SaluteSpeech",
            entry_type=dr.DeviceEntryType.SERVICE,
        )

        self._config_entry = config_entry

    @property
    def supported_languages(self) -> list[str]:
        """Return a list of supported languages."""
        return SUPPORTED_LANGUAGES

    @property
    def default_language(self) -> str:
        """Return the default language."""
        return DEFAULT_LANG

    @property
    def supported_options(self) -> list[str]:
        """Return list of supported options like voice, audio output."""
        return [ATTR_VOICE, ATTR_AUDIO_OUTPUT]

    @property
    def default_options(self) -> dict[str, Any]:
        """Return a dict including default options."""
        return {
            ATTR_VOICE: DEFAULT_VOICE,
            ATTR_AUDIO_OUTPUT: DEFAULT_OUTPUT_CONTAINER,
        }

    @callback
    def async_get_supported_voices(self, language: str) -> list[Voice] | None:
        """Return a list of supported voices for a language."""
        if not (voices := TTS_VOICES.get(language)):
            return None
        return [Voice(voice_id, name) for name, voice_id in voices]

    async def async_get_tts_audio(
        self, message: str, language: str, options: dict[str, Any]
    ) -> TtsAudioType:
        """Get TTS audio from SaluteSpeech."""
        LOGGER.debug("Starting TTS synthesis for message: %s", message)

        output_container = options[ATTR_AUDIO_OUTPUT]
        container_audio_type = TTS_OUTPUT_CONTAINERS.get(
            output_container, TTS_OUTPUT_CONTAINERS[DEFAULT_OUTPUT_CONTAINER]
        )
        voice = options[ATTR_VOICE]

        root_certificates = self._config_entry.runtime_data[DATA_ROOT_CERTIFICATES]
        auth_helper = self._config_entry.runtime_data[DATA_AUTH_HELPER]

        ssl_cred = grpc.ssl_channel_credentials(root_certificates=root_certificates)
        token = await auth_helper.get_access_token()
        token_cred = grpc.access_token_call_credentials(token)

        async with aio.secure_channel(
            "smartspeech.sber.ru:443",
            grpc.composite_channel_credentials(ssl_cred, token_cred),
        ) as channel:
            stub = synthesis_pb2_grpc.SmartSpeechStub(channel)

            try:
                request = self._create_synthesis_request(
                    message, container_audio_type, voice, language
                )
                audio = await self._fetch_audio_data(stub, request)
                if audio:
                    LOGGER.debug("TTS synthesis completed successfully")
                    return (output_container, audio)
                else:
                    LOGGER.error("No audio data received from SaluteSpeech")
                    return (None, None)
            except grpc.RpcError as err:
                LOGGER.error("Error occurred during SaluteSpeech TTS call: %s", err)
                return (None, None)

    def _create_synthesis_request(
        self,
        message: str,
        container_audio_type: synthesis_pb2.SynthesisRequest.AudioEncoding,
        voice: str,
        language: str = DEFAULT_LANG,
    ) -> synthesis_pb2.SynthesisRequest:
        """Create a TTS request."""
        synthesis_options = synthesis_pb2.SynthesisRequest()

        synthesis_options.text = message
        synthesis_options.audio_encoding = container_audio_type
        synthesis_options.voice = f"{voice}_24000"
        synthesis_options.language = language

        return synthesis_options

    async def _fetch_audio_data(
        self, stub, request: synthesis_pb2.SynthesisRequest
    ) -> bytes | None:
        """Fetch audio data from SaluteSpeech."""
        connection = stub.Synthesize(request)

        audio = io.BytesIO()
        async for response in connection:
            if response.data:
                audio.write(response.data)
            else:
                LOGGER.warning("Empty audio chunk received from SaluteSpeech")

        audio.seek(0)
        return audio.read()

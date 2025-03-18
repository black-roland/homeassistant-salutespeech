"""Speech to text using SaluteSpeech."""

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import AsyncGenerator, AsyncIterable, List

import grpc
from grpc import aio
from homeassistant.components.stt import (
    AudioBitRates,
    AudioChannels,
    AudioCodecs,
    AudioFormats,
    AudioSampleRates,
    SpeechMetadata,
    SpeechResult,
    SpeechResultState,
    SpeechToTextEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api.grpc import recognition_pb2, recognition_pb2_grpc
from .const import (
    DATA_AUTH_HELPER,
    DATA_ROOT_CERTIFICATES,
    DOMAIN,
    EVENT_SALUTESPEECH_STT_EMOTIONS,
    LOGGER,
    SUPPORTED_LANGUAGES,
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SaluteSpeech via config entry."""
    async_add_entities([SaluteSpeechSTTEntity(config_entry)])


class SaluteSpeechSTTEntity(SpeechToTextEntity):
    """SaluteSpeech STT entity."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize the entity."""
        self._attr_unique_id = f"{config_entry.entry_id}"
        self._attr_name = config_entry.title
        self._attr_device_info = dr.DeviceInfo(
            identifiers={(DOMAIN, config_entry.entry_id)},
            manufacturer="Sber",
            model="SaluteSpeech",
            entry_type=dr.DeviceEntryType.SERVICE,
        )
        self._config_entry = config_entry

    @property
    def supported_languages(self) -> List[str]:
        """Return a list of supported languages."""
        return SUPPORTED_LANGUAGES

    @property
    def supported_formats(self) -> List[AudioFormats]:
        """Return a list of supported formats."""
        return [AudioFormats.WAV, AudioFormats.OGG]

    @property
    def supported_codecs(self) -> List[AudioCodecs]:
        """Return a list of supported codecs."""
        return [AudioCodecs.PCM, AudioCodecs.OPUS]

    @property
    def supported_bit_rates(self) -> List[AudioBitRates]:
        """Return a list of supported bitrates."""
        return [AudioBitRates.BITRATE_16]

    @property
    def supported_sample_rates(self) -> List[AudioSampleRates]:
        """Return a list of supported samplerates."""
        return [
            AudioSampleRates.SAMPLERATE_8000,
            AudioSampleRates.SAMPLERATE_16000,
            AudioSampleRates.SAMPLERATE_44100,
            AudioSampleRates.SAMPLERATE_48000,
        ]

    @property
    def supported_channels(self) -> List[AudioChannels]:
        """Return a list of supported channels."""
        return [AudioChannels.CHANNEL_MONO]

    async def async_process_audio_stream(
        self, metadata: SpeechMetadata, stream: AsyncIterable[bytes]
    ) -> SpeechResult:
        """Process an audio stream to STT service."""

        async def request_generator() -> (
            AsyncGenerator[recognition_pb2.RecognitionRequest, None]
        ):
            LOGGER.debug("Sending the message with recognition params...")
            recognition_options = self._get_recognition_options(metadata)
            yield recognition_pb2.RecognitionRequest(options=recognition_options)

            async for audio_bytes in stream:
                yield recognition_pb2.RecognitionRequest(audio_chunk=audio_bytes)

        async def recognize_stream(
            stub: recognition_pb2_grpc.SmartSpeechStub,
        ) -> List[str]:
            """Recognize speech from the audio stream."""
            connection = stub.Recognize(request_generator(), metadata=())

            text = None
            async for response in connection:
                if response.HasField("backend_info"):
                    backend_info = response.backend_info
                    LOGGER.debug("Backend info: %s", backend_info)

                if response.HasField("transcription"):
                    transcription = response.transcription

                    if not transcription.eou:
                        continue

                    text = " ".join([hyp.normalized_text for hyp in transcription.results])

                    if transcription.HasField("emotions_result"):
                        self.hass.bus.async_fire(
                            EVENT_SALUTESPEECH_STT_EMOTIONS,
                            {
                                "positive": transcription.emotions_result.positive,
                                "neutral": transcription.emotions_result.neutral,
                                "negative": transcription.emotions_result.negative,
                            },
                        )

            return text

        root_certificates = self._config_entry.runtime_data[DATA_ROOT_CERTIFICATES]
        auth_helper = self._config_entry.runtime_data[DATA_AUTH_HELPER]

        ssl_cred = grpc.ssl_channel_credentials(root_certificates=root_certificates)
        token = await auth_helper.get_access_token()
        token_cred = grpc.access_token_call_credentials(token)
        async with aio.secure_channel(
            "smartspeech.sber.ru:443",
            grpc.composite_channel_credentials(ssl_cred, token_cred),
        ) as channel:
            stub = recognition_pb2_grpc.SmartSpeechStub(channel)
            try:
                transcription = await recognize_stream(stub)
                if not transcription:
                    return SpeechResult(None, SpeechResultState.ERROR)
                return SpeechResult(transcription, SpeechResultState.SUCCESS)
            except grpc.RpcError as err:
                LOGGER.error("Error occurred during speech recognition: %s", err)
                return SpeechResult(None, SpeechResultState.ERROR)

    def _get_recognition_options(
        self, metadata: SpeechMetadata
    ) -> recognition_pb2.RecognitionOptions:
        """Get recognition options based on metadata."""
        options = recognition_pb2.RecognitionOptions()
        options.audio_encoding = recognition_pb2.RecognitionOptions.PCM_S16LE
        options.sample_rate = metadata.sample_rate
        options.channels_count = 1
        # options.language = metadata.language
        return options

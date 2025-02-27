See [description in English below](#salutespeech-integration-for-home-assistant) 👇
<br>
<br>

# Интеграция SaluteSpeech для Home Assistant

[![Добавить репозиторий в HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=black-roland&repository=homeassistant-salutespeech&category=integration) [![Настроить интеграцию](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=salutespeech)

Интеграция SaluteSpeech для Home Assistant предоставляет функциональность распознавания (STT) и синтеза речи (TTS), используя передовые технологии обработки естественного языка от Sber.

SaluteSpeech это облачный сервис.

## Возможности

- **Преобразование речи в текст:**
  - Определение конца высказывания.
  - [Выявление эмоций в диалоге](https://yaml.mansmarthome.info/roland/efff1cbd469c4a1d8e25e721ab388aea).
  - Расстановка знаков препинания и буквы «ё».

- **Преобразование текста в речь:**
  - Генерация речи на русском, английском и казахском языках.
  - Озвучивание текста любой сложности и стиля.
  - Уникальные ML-модели для расстановки ударений и произношения.
  - Нормализация текста для корректного озвучивания адресов, имен, цифр и других сложных слов.

## Подготовка

1. **Регистрация в SaluteSpeech:**
   - Зарегистрируйтесь [в личном кабинете](https://developers.sber.ru/docs/ru/salutespeech/integration-individuals).
   - Создайте проект SaluteSpeech API и сгенерируйте ключ авторизации.

2. **Получение Access Token:**
   - Для доступа к сервису необходимо получить Access Token. Для физических лиц доступен тип использования `SALUTE_SPEECH_PERS`.

## Установка

1. Добавьте репозиторий в HACS: `https://github.com/black-roland/homeassistant-salutespeech` или воспользуйтесь голубой кнопкой выше.
2. Установите пользовательский компонент через HACS.
3. Перезапустите Home Assistant, чтобы завершить установку.

## Настройка

- [Добавьте интеграцию в настройках](https://my.home-assistant.io/redirect/config_flow_start/?domain=salutespeech).
- Введите ваш Access Token и сохраните конфигурацию.
- Настройте SaluteSpeech в качестве движка распознавания (STT) и синтеза речи (TTS) для вашего голосового помощника.

## Поддержка автора

Если эта интеграция была вам полезна, подумайте о том, чтобы [угостить автора чашечкой кофе](https://mansmarthome.info/donate/#donationalerts)! Ваша благодарность ценится!

#### Благодарности

Огромное спасибо всем, кто поддерживает этот проект! Ваш вклад имеет большое значение.

![Спасибо](https://github.com/user-attachments/assets/00e2bd2f-be25-4cae-85ef-3e5fddb8ecbd)

---

# SaluteSpeech Integration for Home Assistant

[![Add custom repository to HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=black-roland&repository=homeassistant-salutespeech&category=integration) [![Set up SaluteSpeech integration](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=salutespeech)

The SaluteSpeech integration for Home Assistant provides speech recognition (STT) and text-to-speech (TTS) functionality using advanced natural language processing technology from Sber.

SpeechKit is a cloud service.

## Features

- **Speech-to-Text:**
  - End-of-speech detection.
  - Emotion detection in dialogue.

- **Text-to-Speech (TTS):**
  - Speech generation in Russian, English, and Kazakh.
  - Pronunciation of texts of any complexity and style.
  - Unique ML models for stress and pronunciation placement.
  - Text normalization for correct pronunciation of addresses, names, numbers, and other complex words.

## Prerequisites

1. **Register in SaluteSpeech:**
   - Register a personal account in the [Studio](https://developers.sber.ru/docs/ru/salutespeech/integration-individuals).
   - Create a SaluteSpeech API project and generate an authorization key.

2. **Obtain Access Token:**
   - To access the service, you need to obtain an Access Token. For individuals, the usage type `SALUTE_SPEECH_PERS` is available.

## Installation

1. Add the repository to HACS (Home Assistant Community Store): `https://github.com/black-roland/homeassistant-salutespeech` or use the blue button above
2. Install the custom component using HACS.
3. Restart Home Assistant to complete the installation.

## Configuration

- [Set up the integration in settings](https://my.home-assistant.io/redirect/config_flow_start/?domain=salutespeech).
- Enter your API key and save the configuration.
- Configure SaluteSpeech as an STT and TTS engine for your Voice assistant.


## Donations

If this integration has been useful to you, consider [buying the author a coffee](https://www.donationalerts.com/r/mansmarthome)! Your gratitude is appreciated!

#### Thank you

![Thank you](https://github.com/user-attachments/assets/00e2bd2f-be25-4cae-85ef-3e5fddb8ecbd)

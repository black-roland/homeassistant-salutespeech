See [description in English below](#salutespeech-integration-for-home-assistant) 👇
<br>
<br>

# Интеграция SaluteSpeech для Home Assistant

[![Добавить репозиторий в HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=arturgadelshin&repository=homeassistant-salutespeech&category=integration) [![Настроить интеграцию](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=salutespeech)

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

If this integration has been useful to you, consider [buying the author a coffee](https://www.donationalerts.com/r/mansmarthome)! Your gratitude is appreciated!

#### Thank you

![Thank you](https://github.com/user-attachments/assets/00e2bd2f-be25-4cae-85ef-3e5fddb8ecbd)

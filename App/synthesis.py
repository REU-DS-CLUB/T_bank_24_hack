import os
import grpc
from tinkoff.cloud.tts.v1 import tts_pb2_grpc, tts_pb2
import wave


# Функция для синтеза речи и возвращения аудио в байтах
def synthesize_speech(text, voice_name):
    # Получение токена из переменной окружения
    api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InIxUGNSUGsvMVo3WG9QSGxIS3d2cmdWUkxnQ1ZFTnByRHZPK1ArODM2NHM9VFRTX1RFQU0ifQ.eyJpc3MiOiJ0ZXN0X2lzc3VlciIsInN1YiI6InRlc3RfdXNlciIsImF1ZCI6InRpbmtvZmYuY2xvdWQudHRzIiwiZXhwIjoxNzMwMDQxOTExfQ.uyK_tn9z_ShLwBaIc1AfV8DaGfEOC0SbDbQwzsqBc3s"

    if not api_token:
        raise ValueError("API ключ не найден. Установите переменную окружения AUTH_TOKEN.")

    # Подключение через gRPC
    endpoint = "api.tinkoff.ai:443"
    credentials = grpc.ssl_channel_credentials()
    channel = grpc.secure_channel(endpoint, credentials)
    stub = tts_pb2_grpc.TextToSpeechStub(channel)

    # Запрос на синтез речи
    request = tts_pb2.SynthesizeSpeechRequest(
        input=tts_pb2.SynthesisInput(text=text),
        audio_config=tts_pb2.AudioConfig(audio_encoding=tts_pb2.LINEAR16, sample_rate_hertz=16000),
        voice=tts_pb2.VoiceSelectionParams(name=voice_name),
    )

    # Отправление запроса с API ключом
    metadata = [("authorization", f"Bearer {api_token}")]
    response = stub.Synthesize(request, metadata=metadata)

    # Возврат содержимого аудио в байтах
    return response.audio_content


# Создание WAV-файла с объединенными репликами
def create_wav(dialogue_text):
    voices = {
        "Папа": "dorofeev",
        "Дочка": "sveta"
    }

    dialogue = list()

    for line in dialogue_text.split("\n"):
        if ":" in line:
            speaker, phrase = line.split(':', 1)
            dialogue.append((speaker, phrase))

    with wave.open("App/files/full_dialogue.wav", "wb") as output_wave:
        output_wave.setnchannels(1)  # моно
        output_wave.setsampwidth(2)  # 16 бит
        output_wave.setframerate(16000)

        # Пауза перед первой репликой (0.3 секунды тишины)
        silence_before_first = b'\x00\x00' * int(0.3 * 16000)
        output_wave.writeframes(silence_before_first)

        # Синтез каждой реплики с добавлением в итоговый файл
        for speaker, text in dialogue:
            voice_name = voices.get(speaker.strip(), "sveta")  # По умолчанию голос Дочки
            audio_content = synthesize_speech(text, voice_name)

            # Запись аудио в итоговый файл
            output_wave.writeframes(audio_content)

        # Пауза после последней реплики (1 секунда тишины)
        silence_after_last = b'\x00\x00' * 16000
        output_wave.writeframes(silence_after_last)


if __name__ == "__main__":
    create_wav("Дочка: Привет, мне попалась интересная статья, и я хотела бы в ней разобраться! Можешь помочь?\nПапа: Хорошо. Конечно могу.")

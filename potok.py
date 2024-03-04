import struct, pyaudio
import numpy as np
from transformers import pipeline

FORMAT = pyaudio.paInt16  # глубина звука = 16 бит = 2 байта
CHANNELS = 1  # моно
RATE = 44100  # частота дискретизации - кол-во фреймов в секунду
CHUNK = 2048  # кол-во фреймов за один "запрос" к микрофону - тк читаем по кусочкам

audio = pyaudio.PyAudio()

def transcribe_audio(data):
    transcriber = pipeline(model="openai/whisper-tiny", generate_kwargs={"language": "english"})
    try:
        resp = transcriber(data)['text']
        return resp
    except Exception as e:
        return e

stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
print("запись...")

# каждую секунду
while True:
    s = 0 

    # для каждого "запроса"
    for j in range(RATE // CHUNK):
        data = stream.read(CHUNK)

        frames = struct.unpack("<" + str(CHUNK) + "h", data)
        for frame in frames:
            s += abs(frame)

        audio_data = np.frombuffer(data, dtype=np.int16)

    print(s // RATE, '+', transcribe_audio(audio_data))
    # stop_stream(audio_data)
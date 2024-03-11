import asyncio
import numpy as np
import pyaudio
from transformers import pipeline
import keyboard
import librosa

CHUNK = 1023                    # форма аудиосигнала
FRT = pyaudio.paFloat32         # значение амплитуды
ORIGINAL_RATE = 44100           # исходная частота дискретизации
NEW_RATE = 16000                # новая частота дискретизации

p = pyaudio.PyAudio()

# Функция для преобразования аудио в текст
async def transcribe_audio():
    try:
        transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-small", generate_kwargs={"language": "russian"})
        stream = p.open(format=FRT, channels=1, rate=ORIGINAL_RATE, input=True, frames_per_buffer=CHUNK)

        print("Слушаем...")
        all_data = np.array([])

        while i<300:
            data = stream.read(CHUNK)
            numpy_data = np.frombuffer(data, dtype=np.float32)

            all_data = np.append(all_data, numpy_data)
            i+=1
            # Остановка после нажатия Enter
            if keyboard.is_pressed(hotkey='Enter'):
                break

        print("Остановлено.")
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Модель
        transcription = transcriber(librosa.resample(all_data, orig_sr=ORIGINAL_RATE, target_sr=NEW_RATE)).get("text")
        if transcription:
            print("Текст:", transcription)

    except Exception as e:
        print(e)

async def main():                   
    await asyncio.gather(transcribe_audio())

if __name__ == "__main__":
    asyncio.run(main())
import wave
import pyaudio
import asyncio
from transformers import pipeline

CHUNK = 1024                    # форма аудиосигнала
FRT = pyaudio.paInt32           # значение амплитуды
RT = 44100                      # частота 
OUTPUT = 'out.wav'

STOP_FLAG = False
p = pyaudio.PyAudio()

async def save_frames(frames):   # АСИНХРОННОЕ СОЗДАНИЕ .WAV ФАЙЛА
    with wave.open(OUTPUT, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(p.get_sample_size(FRT))
        w.setframerate(RT)
        w.writeframes(b''.join(frames))

async def record_audio(stop_event): # АСИНХРОННАЯ ЗАПИСЬ АУДИО
    stream = p.open(format=FRT, channels=1, rate=RT, input=True, frames_per_buffer=CHUNK)
    frames = []

    print('Записываем...')
    while not stop_event.is_set():
        data = stream.read(CHUNK)
        frames.append(data)

    print('Запись сделана!')
    stream.stop_stream()
    stream.close()
    p.terminate()

    await save_frames(frames)   # Асинхронный вызов функции сохранения
    await open_wav()            # Асинхронный вызов функции открытия

async def open_wav():           # АСИНХРОННОЕ ОТКРЫТИЕ ФАЙЛА
    try:
        transcriber = pipeline(model="openai/whisper-large", generate_kwargs={"language": "russian"})
        print(transcriber(OUTPUT)['text'])  # json
    except Exception as e:
        print(e)

async def stop_input():         # Функция для завершения записи
    global STOP_FLAG
    input('Для завершения записи нажмите Enter\n')
    STOP_FLAG = True

async def main():               # Основная асинхронная функция
    stop_event = asyncio.Event()
    record_task = asyncio.create_task(record_audio(stop_event))
    stop_task = asyncio.create_task(stop_input())

    await asyncio.gather(record_task, stop_task)

if __name__ == '__main__':
    asyncio.run(main())          # Запуск основной асинхронной функции
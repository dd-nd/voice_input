import speech_recognition as sr
import pyaudio
import wave
import sys
import threading
from transformers import pipeline


CHUNK = 1024    # определяет форму аудиосигнала
FRT = pyaudio.paInt32   # значение амплитуды
RT = 44100      # частота 
OUTPUT = 'out.wav'
STOP_SYMBOL = ''

p = pyaudio.PyAudio()


def save_frames(frame):    # СОЗДАНИЕ .WAV ФАЙЛА (1)
    with wave.open(OUTPUT, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(p.get_sample_size(FRT))
        w.setframerate(RT)
        w.writeframes(b''.join(frame))


def record_audio():     # ЗАПИСЬ АУДИО (2)
    stream = p.open(format=FRT, channels=1, rate=RT, input=True, frames_per_buffer=CHUNK)
    print('идет запись...')
    frames = []

    while STOP_SYMBOL != '/':
        data = stream.read(CHUNK)
        frames.append(data)

    print('запись выполнена!')
    stream.stop_stream()
    stream.close()
    p.terminate()

    save_frames(frame=frames)   # (1)
    open_wav()  # (3)


def open_wav():     # ОТКРЫТИЕ ФАЙЛА (3)
    try:
        transcriber = pipeline(model="openai/whisper-medium", generate_kwargs={"language": "russian"})
        print(transcriber(OUTPUT)['text'])  # json {'text':'...value...'}
    except Exception as e:
        print(e)

def stop_input():
    global STOP_SYMBOL

    print('для остановки записи введите /')
    STOP_SYMBOL = sys.stdin.read(1)


if __name__ == '__main__':
    audio_thread = threading.Thread(target=record_audio)
    stop_thread = threading.Thread(target=stop_input)

    audio_thread.start()
    stop_thread.start()

    audio_thread.join()
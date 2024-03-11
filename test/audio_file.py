import threading
import wave
import pyaudio
from transformers import pipeline

CHUNK = 1024                    # форма аудиосигнала
FRT = pyaudio.paInt32           # значение амплитуды
RT = 44100                      # частота 
OUTPUT = 'out.wav'

STOP_SYMBOL = threading.Event()
p = pyaudio.PyAudio()

def save_frames(frames):        # СОЗДАНИЕ .WAV ФАЙЛА (1)
    # with io.BytesIO() as wav_file:
    #     with wave.open(wav_file, 'wb') as w:
    with wave.open(OUTPUT, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(p.get_sample_size(FRT))
        w.setframerate(RT)
        w.writeframes(b''.join(frames))


def record_audio():             # ЗАПИСЬ АУДИО (2)
    stream = p.open(format=FRT, channels=1, rate=RT, input=True, frames_per_buffer=CHUNK)
    frames = []

    print('Записываем...')
    while not STOP_SYMBOL.is_set():
        data = stream.read(CHUNK)
        frames.append(data)

    print('Запись сделана!')
    stream.stop_stream()
    stream.close()
    p.terminate()

    save_frames(frames)         # (1)
    open_wav()                  # (3)


def open_wav():                 # ОТКРЫТИЕ ФАЙЛА (3)
    try:
        transcriber = pipeline(model="openai/whisper-tiny", generate_kwargs={"language": "russian"})
        print(transcriber(OUTPUT)['text'])  # json
    except Exception as e:
        print(e)


def stop_input():
    input('Для завершения записи нажмине Enter\n')
    STOP_SYMBOL.set()


if __name__ == '__main__':
    audio_thread = threading.Thread(target=record_audio)
    stop_thread = threading.Thread(target=stop_input)

    audio_thread.start()
    stop_thread.start()

    audio_thread.join()
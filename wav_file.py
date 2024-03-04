from transformers import pipeline
import threading
import io
import wave
import pyaudio
import numpy as np

CHUNK = 1024                    # форма аудиосигнала
FRT = pyaudio.paInt16           # значение амплитуды
RT = 44100                      # частота 

STOP_SYMBOL = threading.Event()
p = pyaudio.PyAudio()

# Сохранение фреймов в io файл
def save_data(frames):
    with io.BytesIO() as wav_file:
        with wave.open(wav_file, 'wb') as w:
            w.setnchannels(1)
            w.setsampwidth(p.get_sample_size(FRT))
            w.setframerate(RT)
            w.writeframes(b''.join(frames))

        # Чтение io файла и преобразование в массив numpy
        wav_file.seek(0)  # Устанавливаем указатель файла на начало
        with wave.open(wav_file, 'rb') as w:
            frames = w.readframes(w.getnframes())  # Чтение кадров из файла
            samples = np.frombuffer(frames, dtype=np.int16)  # Преобразование в массив NumPy
    return samples

# Speech to text
def transformation_frames(data):
    try:
        transcriber = pipeline(model="openai/whisper-small", 
                               task="automatic-speech-recognition", 
                               generate_kwargs={"language":"russian", 
                                                "do_sample":False
                                                # , "temperature":0.1
                                                })
        return(transcriber(data)['text'])
    except Exception as e:  
        return str(e)

# Остановка записи по нажатии клавиши
def stop_input():
    input('Для завершения записи нажмине Enter\n')
    STOP_SYMBOL.set()

# Запись аудио
def record_audio():
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

    ready_data = save_data(frames)
    # ready_data = reading_bytesIO(saved_data)
    # print(ready_data)
    # print(transformation_frames(ready_data))
    text = transformation_frames(ready_data)
    print(text)


if __name__ == '__main__':
    audio_thread = threading.Thread(target=record_audio)
    stop_thread = threading.Thread(target=stop_input)

    audio_thread.start()
    stop_thread.start()

    audio_thread.join()
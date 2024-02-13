import speech_recognition as sr
import pyaudio
import wave
import sys
import threading

CHUNK = 1024    # определяет форму аудиосигнала
FRT = pyaudio.paInt16   # значение амплитуды
RT = 44100      # частота 
REC_SEC = 5     #длина записи
OUTPUT = 'out.wav'

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

    for i in range(0, int(RT / CHUNK * REC_SEC)):
        data = stream.read(CHUNK)
        frames.append(data)

    print('запись выполнена!')
    stream.stop_stream()
    stream.close()
    p.terminate()

    save_frames(frame=frames)   # (1)


def open_wav():     # ОТКРЫТИЕ ФАЙЛА (3)
    record_file = sr.WavFile(OUTPUT)
    r = sr.Recognizer()

    with record_file as audio:
        try:
            r.adjust_for_ambient_noise(audio)
            print(r.recognize_google(r.record(audio), language='ru-RU'))
        except sr.UnknownValueError:
            print('Не удалось распознать речь')
        except sr.RequestError as e:
            print(f'Ошибка при обращении к сервису распознавания речи; {e}')


if __name__ == '__main__':
    record_audio()  # (2) ->> (1)
    open_wav()  # (3)





# ОРИГИНАЛ (РАБОТАЕТ)
# # запись аудио
# stream = p.open(format=FRT, channels=1, rate=RT, input=True, frames_per_buffer=CHUNK)
# print('идет запись')
# frames = []

# for i in range(0, int(RT / CHUNK * REC_SEC)):
#     data = stream.read(CHUNK)
#     frames.append(data)

# print('запись выполнена')
# stream.stop_stream()

# stream.close()
# p.terminate()
        


# воспроизведение записи
# with wave.open(OUTPUT, 'rb') as wf:
#     def callback(in_data, frame_count, time_info, status):
#         data = wf.readframes(frame_count)
#         return (data, pyaudio.paContinue)

#     p = pyaudio.PyAudio()

#     stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#                     channels=wf.getnchannels(),
#                     rate=wf.getframerate(),
#                     output=True,
#                     stream_callback=callback)

#     while stream.is_active():
#         time.sleep(0.1)

#     stream.close()
#     p.terminate()
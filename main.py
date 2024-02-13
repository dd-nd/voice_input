import speech_recognition as sr
import pyaudio
import wave

CHUNK = 1024    # определяет форму ауди сигнала
FRT = pyaudio.paInt16   # 16-битный формат -- значение амплитуды
CHAN = 1        # канал записи звука
RT = 44100      # частота 
REC_SEC = 5     #длина записи
OUTPUT = 'out.wav'

p = pyaudio.PyAudio()

# запись аудио
stream = p.open(format=FRT, channels=CHAN, rate=RT, input=True, frames_per_buffer=CHUNK)
print('идет запись')
frames = []

for i in range(0, int(RT / CHUNK * REC_SEC)):
    data = stream.read(CHUNK)
    frames.append(data)

print('запись выполнена')
stream.stop_stream()

stream.close()
p.terminate()

# запись в файл
with wave.open(OUTPUT, 'wb') as w:
    w.setnchannels(CHAN)
    w.setsampwidth(p.get_sample_size(FRT))
    w.setframerate(RT)
    w.writeframes(b''.join(frames))
# w.close()

# открытие файда
record_file = sr.WavFile(OUTPUT)
r = sr.Recognizer()

with record_file as audio:
    try:
        text = r.record(audio)
        r.adjust_for_ambient_noise(audio)
        text = r.recognize_google(audio, language='ru-RU')
        print(text)
    except sr.UnknownValueError:
        print('Не удалось распознать речь')
    except sr.RequestError as e:
        print(f'Ошибка при обращении к сервису распознавания речи; {e}')
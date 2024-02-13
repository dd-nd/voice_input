import speech_recognition as sr
import pyaudio
import wave
import params as par

p = pyaudio.PyAudio()

# запись аудио
with p.open(format=par.FRT, channels=par.CHAN, rate=par.RT, 
            input=True, frames_per_buffer=par.CHUNK) as stream:
    print('идет запись')
    frames = []

    for i in range(0, int(par.RT / par.CHUNK * par.REC_SEC)):
        data = stream.read(par.CHUNK)
        frames.append(data)

    print('запись выполнена')
    stream.stop_stream()
# stream.close()
p.terminate()

# запись в файл
with wave.open(par.OUTPUT, 'wb') as w:
    w.setnchannels(par.CHAN)
    w.setsampwidth(p.get_sample_size(par.FRT))
    w.setframerate(par.RT)
    w.writeframes(b''.join(frames))
# w.close()

# открытие файда
record_file = sr.WavFile(par.OUTPUT)
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
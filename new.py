import numpy as np
import pyaudio
from transformers import pipeline, AutoTokenizer

chunk = 1024
frt = pyaudio.paInt32
original_rate = 44100
new_rate = 16000

p = pyaudio.PyAudio()
# tokenizer = AutoTokenizer.from_pretrained("openai/whisper-small")

# special_tokens = ["<SPECIAL1>", "<SPECIAL2>", "<SPECIAL3>"]
# num_added_tokens = tokenizer.add_special_tokens({"additional_special_tokens": special_tokens})


# Функция для понижения частоты дискретизации и записи в массив np
def downsample_and_record():
    decimation_factor = int(original_rate / new_rate)
    # data = b''
    
    stream = p.open(format=frt, channels=1, rate=original_rate, input=True, frames_per_buffer=chunk)
    audio_data = stream.read(chunk)
    print('запись')

    for i in range(300):
        decimated_audio_data = audio_data[::decimation_factor]
        # print('понижение')
        numpy_audio_data = np.frombuffer(decimated_audio_data, dtype=np.int32)
        # print('преобразование')
        i+=1
        # data += numpy_audio_data
        audio_data = stream.read(chunk)
        # print('чтение следующего куска')

    stream.stop_stream()
    stream.close()
    p.terminate()
    print('закрытие')
    return np.frombuffer(numpy_audio_data, dtype=np.int32)

# Функция преобразования
def transcribing():
    try:
        transcriber = pipeline('automatic-speech-recognition', model="openai/whisper-small", generate_kwargs={"language": "russian", "task":"transcribe"})
        recorded_data = downsample_and_record()
        return(transcriber(recorded_data))
    except Exception as e:
        return str(e)

a = transcribing()
print(a)
from flask import Flask, jsonify
from flask_cors import CORS
import asyncio
import numpy as np
import pyaudio
from transformers import pipeline
import keyboard
from waitress import serve
import librosa

CHUNK = 1024                    # форма аудиосигнала
FRT = pyaudio.paFloat32         # значение амплитуды
ORIGINAL_RATE = 44100           # исходная частота дискретизации
NEW_RATE = 16000                # новая частота дискретизации

app = Flask(__name__)
CORS(app)

p = pyaudio.PyAudio()

# Функция для преобразования аудио в текст
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3", generate_kwargs={"language": "russian"})
        stream = p.open(format=FRT, channels=1, rate=ORIGINAL_RATE, input=True, frames_per_buffer=CHUNK)

        print("Слушаем...")
        all_data = np.array([])

        while True:
            data = stream.read(CHUNK)
            numpy_data = np.frombuffer(data, dtype=np.float32)

            all_data = np.append(all_data, numpy_data)
           
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
            response = jsonify({'transcription': transcription})
            response.headers['Access-Control-Allow-Origin'] = '*'  # Устанавливаем заголовок для CORS
            return response
    except Exception as e:
        return jsonify({'error': str(e)})

# async def main():                   
#     await asyncio.gather(transcribe_audio())

if __name__ == "__main__":
    # app.run(debug=True)
    serve(app, host="0.0.0.0", port=8080)
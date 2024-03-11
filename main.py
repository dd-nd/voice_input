from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
from transformers import pipeline
from waitress import serve
import librosa

ORIGINAL_RATE = 44100           # исходная частота дискретизации
NEW_RATE = 16000                # новая частота дискретизации

app = Flask(__name__)
transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-tiny", generate_kwargs={"language": "russian"})
CORS(app)

# Функция для преобразования аудио в текст
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        # Обработка не конечных значений
        # data[~np.isfinite(data)] = 0
        
        data = np.frombuffer(request.data, dtype=np.float32)

        # Модель
        transcription = transcriber(librosa.resample(data, orig_sr=ORIGINAL_RATE, target_sr=NEW_RATE)).get("text")
        if transcription:
            response = jsonify({'transcription': transcription})
            response.headers['Access-Control-Allow-Origin'] = '*'  # Заголовок для CORS
            return response
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    serve(app, host="127.0.0.1", port=8800)
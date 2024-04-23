from flask import Flask, jsonify, request, render_template
from transformers import pipeline
from waitress import serve
import asyncio
import numpy as np
import pyaudio
from transformers import pipeline
import keyboard
import librosa


CHUNK = 1023                    # форма аудиосигнала
FRT = pyaudio.paFloat32         # значение амплитуды
ORIGINAL_RATE = 44100           # исходная частота дискретизации
NEW_RATE = 16000                # новая частота дискретизации

p = pyaudio.PyAudio()

app = Flask(__name__)
transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-tiny", generate_kwargs={"language": "russian"})

all_data = np.array([])
is_running = False  # Флаг для управления циклом

# Функция начала записи
@app.route('/startRecording', methods=['POST'])
def startRecording():
    try:
        global is_running, all_data
        if not is_running:
            is_running = True
            stream = p.open(format=FRT, channels=1, rate=ORIGINAL_RATE, input=True, frames_per_buffer=CHUNK)
            while is_running:
                if is_running != False:
                    data = stream.read(CHUNK)
                    numpy_data = np.frombuffer(data, dtype=np.float32)
                    all_data = np.append(all_data, numpy_data)
            return jsonify({ 'message': f'Цикл остановлен {is_running}' }), 200
        else:
            stopRecording(stream=stream)
            return jsonify({ 'message': 'Запись уже запущена' }), 400
    except Exception as e:
        return jsonify({ 'error': str(e) }), 500


# Функция завершения записи
@app.route('/stopRecording', methods=['POST'])
def stopRecording(stream):
    global is_running
    is_running = False
    if not is_running:
        stream.stop_stream()
        stream.close()
        p.terminate()
    return jsonify({ 'message': 'Цикл остановлен' }), 200


# # Функция для преобразования аудио в текст
# @app.route('/transcribe', methods=['POST'])
# def transcribe_audio():
#     try:
#         audio_file = request.files['audio']
#         if audio_file.filename == '':
#             return jsonify({'error': 'No file selected'}), 400

#         audio_file.seek(0)
#         audio_data = audio_file.read()  
        
#         transcription = transcriber(audio_data).get('text')
        
#         response = jsonify({'transcription': transcription})
        
#         return response
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500    




@app.route('/')
def main():
    return render_template('index.html')


if __name__ == "__main__":
    serve(app, host="127.0.0.1", port=8800, threads=4)
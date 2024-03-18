from flask import Flask, jsonify, request, render_template
from transformers import pipeline
from waitress import serve

app = Flask(__name__)
transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-tiny", generate_kwargs={"language": "russian"})

@app.route('/')
def main():
    return render_template('index.html')

# Функция для преобразования аудио в текст
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        audio_file.seek(0)
        audio_data = audio_file.read()  
        
        transcription = transcriber(audio_data).get('text')
        
        response = jsonify({'transcription': transcription})
        
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500    

if __name__ == "__main__":
    serve(app, host="127.0.0.1", port=8800)
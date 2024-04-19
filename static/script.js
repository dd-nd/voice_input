let recorder;
let audioChunks = [];
let intervalId;

function startRecording() {
    audioChunks = [];
    navigator.mediaDevices
    .getUserMedia({ audio: true })
    .then((stream) => {
        recorder = new MediaRecorder(stream, { audioBitsPerSecond: 16000 });

        recorder.ondataavailable = (e) => {
            if (e.data.size > 0) {
                audioChunks.push(e.data);
            }
        };

        recorder.start();
        document.getElementById('startButton').style.display = 'none';
        document.getElementById('stopButton').style.display = 'inline';
        document.getElementById('recordingIndicator').style.display = 'inline';
        document.getElementById('stopButton').disabled = false;

        intervalId = setInterval(() => {
            sendAudioData();
        }, 3000);
    })
    .catch((error) => {
        console.error('Error accessing microphone:', error);
    });
}

let isNewResponseReceived = false;

function sendAudioData() {
    if (recorder.state === 'recording') {
        recorder.requestData();
    }

    recorder.ondataavailable = (e) => {
        audioChunks.push(e.data);
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('audio', audioBlob, 'audio.wav');

        fetch('/transcribe', {
            method: 'POST',
            body: formData,
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error('Ошибка при отправке аудио.');
            }
            return response.json();
        })
        .then((data) => {
            if (isNewResponseReceived) {
                document.getElementById('transcriptionResult').innerText += data.transcription;
            } else {
                document.getElementById('transcriptionResult').innerText = data.transcription;
                isNewResponseReceived = true;
            }
        })
        .catch((error) => {
            document.getElementById('transcriptionResult').innerText = 'Ошибка: ' + error.message;
        });
    };
}

function stopRecording() {
    clearInterval(intervalId);
    
    recorder.onstop = () => {
        document.getElementById('startButton').style.display = 'inline';
        document.getElementById('stopButton').style.display = 'none';
        document.getElementById('recordingIndicator').style.display = 'none';
        document.getElementById('stopButton').disabled = true;
        isNewResponseReceived = false; // Сброс флага при остановке записи
        sendAudioData();
        
    };
    recorder.stop();
}
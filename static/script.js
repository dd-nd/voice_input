let recorder;
let audioChunks = [];

// Функция начала записи
async function startRecording() {
  audioChunks = [];
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    recorder = new MediaRecorder(stream);
    recorder.ondataavailable = (e) => {
      audioChunks.push(e.data);
    };
    recorder.start();
    document.getElementById('startButton').style.display = 'none';
    document.getElementById('stopButton').style.display = 'inline';
    document.getElementById('recordingIndicator').style.display = 'inline';
    document.getElementById('stopButton').disabled = false;

    await new Promise((resolve) => {
      setTimeout(() => {
        pauseRecording();
        resolve();
      }, 3000); // Задержка в 3 секунды
    });
  } catch (error) {
    console.error('Error accessing microphone:', error);
  }
}

// Функция остановки
async function pauseRecording() {
  recorder.stop();
  await new Promise((resolve) => {
    recorder.onstop = () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
      sendAudioData(audioBlob);
      startRecording(); 
      resolve();
    };
  });
}

// Функция завершения
async function stopRecording() {
  recorder.stop();
  await new Promise((resolve) => {
    recorder.onstop = () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
      sendAudioData(audioBlob);
      document.getElementById('startButton').style.display = 'inline';
      document.getElementById('stopButton').style.display = 'none';
      document.getElementById('recordingIndicator').style.display = 'none';
      document.getElementById('stopButton').disabled = true;
      resolve();
    };
  });
}

// Функция отправки
async function sendAudioData(blob) {
  try {
    let formData = new FormData();
    formData.append("audio", blob);
    const response = await fetch('/transcribe', {
      method: 'POST',
      body: formData,
    });
    const data = await response.json();
    document.getElementById('transcriptionResult').innerText += data.transcription;
  } catch (error) {
    document.getElementById('transcriptionResult').innerText = 'Error: ' + error.message;
  }
}
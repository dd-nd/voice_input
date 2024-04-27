let recorder;
let audioChunks = [];
const socket = new WebSocket('ws://127.0.0.1:8080/ws');

socket.onopen = function(event) {
  console.log('WebSocket connection established.');
};

socket.onerror = function(error) {
  console.error('WebSocket error: ' + error);
};

// Функция отправки
async function sendAudioData(blob) {
  try {
    if (socket.readyState === WebSocket.OPEN) {
      socket.send(blob);
    }
    
    socket.onmessage = function(event) {
      const data = JSON.parse(event.data);
      document.getElementById('transcriptionResult').innerText += data.transcription;
    };

    socket.onerror = function (error) {
      document.getElementById('transcriptionResult').innerText = 'Error: ' + error.message;
    };
  } catch (error) {
    document.getElementById('transcriptionResult').innerText = 'Error: ' + error.message;
  }
}

async function startRecording() {
  audioChunks = [];
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true }, { audioBitsPerSecond: 16000 });
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
from fastapi import FastAPI, WebSocket, UploadFile, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from transformers import pipeline
import uvicorn

app = FastAPI()
connected_websockets = set()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-tiny", generate_kwargs={"language": "russian"})


class AudioTranscriber:
    def transcribe_audio(self, audio_data: UploadFile):
        try:
            if not audio_data:
                return {'error': 'Empty file'}, 400
            
            transcription = transcriber(audio_data).get('text')
            
            if not transcription:
                return {'error': 'Transcription failed'}, 500
            
            return {'transcription': transcription}
        
        except Exception as e:
            error_message = f'Exception occurred: {str(e)}'
            return {'error': error_message}, 500


@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.websocket("/ws")
async def websocket_transcribe(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            audio_data = await websocket.receive_bytes()
            response = AudioTranscriber().transcribe_audio(audio_data)
            await websocket.send_json(response)
    except Exception as e:
        await websocket.close(code=1001, reason=str(e))
        raise e

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
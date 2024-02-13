import pyaudio

CHUNK = 1024    # определяет форму ауди сигнала
FRT = pyaudio.paInt16   # 16-битный формат -- значение амплитуды
CHAN = 1        # канал записи звука
RT = 44100      # частота 
REC_SEC = 5     #длина записи
OUTPUT = 'out.wav'
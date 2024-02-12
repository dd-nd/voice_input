import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("говорите")
    recognizer.adjust_for_ambient_noise(source)
    audio_data = recognizer.listen(source)

    print("молчите для остановки записи")
    try:
        text = recognizer.recognize_google(audio_data, language="ru-RU")
        print("сказано: " + text)
    except sr.UnknownValueError:
        print("ошибка: Голос не распознан")
    except sr.RequestError as e:
        print(f"ошибка сервиса распознавания речи; {e}")
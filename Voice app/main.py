import speech_recognition as sr
from gtts import gTTS
import os

def recognize_speech_from_mic(recognizer, microphone):
    # Check if recognizer and microphone arguments are appropriate
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("Recognizer must be an instance of sr.Recognizer")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("Microphone must be an instance of sr.Microphone")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Say something:")
    response = recognize_speech_from_mic(recognizer, microphone)

    if response["success"]:
        print("You said: {}".format(response["transcription"]))
        tts = gTTS(text=response["transcription"], lang='en')
        tts.save("response.mp3")
        os.system("mpg321 response.mp3")
    else:
        print("I didn't catch that. What did you say?\nError: {}".format(response["error"]))

if __name__ == "__main__":
    main()

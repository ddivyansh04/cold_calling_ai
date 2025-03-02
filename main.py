import sounddevice as sd
import queue
import vosk
import json
from gtts import gTTS
import os
from transformers import AutoTokenizer, AutoModelForMaskedLM

# Speech-to-Text Setup
q = queue.Queue()
model = vosk.Model("models/vosk_model")

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def listen():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                            channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, 16000)
        print("🎙️ Listening...")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result.get("text", "")

# Text-to-Speech
def speak(text):
    print(f"🗣️ {text}")
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    os.system("ffplay -nodisp -autoexit output.mp3")

# LLM Placeholder
tokenizer = AutoTokenizer.from_pretrained("ai4bharat/indic-bert")
model_llm = AutoModelForMaskedLM.from_pretrained("ai4bharat/indic-bert")

def demo_scheduling():
    speak("Namaste! Kya aapko humare ERP system ka demo schedule karna hai?")
    response = listen()
    if "haan" in response:
        speak("Great! Kal subah 11 baje demo schedule kar dete hai.")
    else:
        speak("Koi baat nahi. Aap jab chahein bataye.")

def candidate_interview():
    speak("Hello! Yeh ek short interview hai. Aapka naam bataiye.")
    name = listen()
    speak(f"Shukriya {name}. Python experience kitna hai?")
    experience = listen()
    speak(f"Thanks! Aapko result email se mil jayega.")

def payment_follow_up():
    speak("Namaste! Aapka ₹5000 ka payment pending hai. Kab tak release karenge?")
    response = listen()
    speak("Thank you! Payment receive hone par confirmation bhejenge.")

def main():
    speak("Kaunsa service chahiye? Demo, Interview ya Payment?")
    service = listen()
    if "demo" in service:
        demo_scheduling()
    elif "interview" in service:
        candidate_interview()
    elif "payment" in service:
        payment_follow_up()
    else:
        speak("Sorry, mujhe samajh nahi aaya.")

if __name__ == "__main__":
    main()

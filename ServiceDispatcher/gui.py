import Tkinter as tk

from Utils.Utils import send, isRetro

class WizardOfOzInterface():
    def __init__(self, root):
        self.root = root
        self.root.title("Wizard of Oz Interface")

        emotions_frame = tk.Frame(self.root)
        emotions_frame.pack()

        emotions_label = tk.Label(emotions_frame, text="Emotions")
        emotions_label.pack()

        self.emotions_data = {
            "calm": tk.DoubleVar(value=0.0),
            "anger": tk.DoubleVar(value=0.0),
            "joy": tk.DoubleVar(value=0.0),
            "sorrow": tk.DoubleVar(value=0.0),
            "laughter": tk.DoubleVar(value=0.0),
            "excitement": tk.DoubleVar(value=0.0),
            "surprise": tk.DoubleVar(value=0.0),
            "attention": tk.DoubleVar(value=0.0),
        }

        for emotion, value in self.emotions_data.items():
            emotion_label = tk.Label(emotions_frame, text=emotion)
            emotion_label.pack()

            emotion_entry = tk.Entry(emotions_frame, textvariable=value)
            emotion_entry.pack()

        send_emotions_button = tk.Button(emotions_frame, text="Send face emotions", command=self.get_emotions)
        send_emotions_button.pack()

        # Speech Section
        speech_frame = tk.Frame(self.root)
        speech_frame.pack()

        speech_label = tk.Label(speech_frame, text="Speech")
        speech_label.pack()

        self.speech_entry = tk.Entry(speech_frame)
        self.speech_entry.pack()

        self.voice_emotion_data = {
            "calm": tk.DoubleVar(value=0.0),
            "anger": tk.DoubleVar(value=0.0),
            "joy": tk.DoubleVar(value=0.0),
            "sorrow": tk.DoubleVar(value=0.0)
        }

        for voice_emotion, value in self.voice_emotion_data.items():
            voice_emotion_label = tk.Label(speech_frame, text=voice_emotion)
            voice_emotion_label.pack()

            voice_emotion_entry = tk.Entry(speech_frame, textvariable=value)
            voice_emotion_entry.pack()

        send_speech_button = tk.Button(speech_frame, text="Send speech", command=self.send_speech)
        send_speech_button.pack()

        # Accident Detection Section
        accident_frame = tk.Frame(self.root)
        accident_frame.pack()

        detect_accident_button = tk.Button(accident_frame, text="Detect accident", command=self.detect_accident)
        detect_accident_button.pack()

    def get_emotions(self):
        emotions_info = {}
        for emotion, value in self.emotions_data.items():
            emotions_info[emotion] = value.get()
        return emotions_info
        
    def send_speech(self):
        speech_text = self.speech_entry.get()
        voice_emotions_info = {}
        params =  {"text":speech_text}
        for voice_emotion, value in self.voice_emotion_data.items():
            voice_emotions_info[voice_emotion] = value.get()
        if isRetro["value"]:
            params["retro"] = params["text"]
        send(-1, "SPEECHENGINE", "talk",params, False)
        send(-1, "SPEECHENGINE","activateSentimentAnalysis", {"voiceEmotions":voice_emotions_info}, False)
        

    def detect_accident(self):
        send(-1, "RAWVIDEO" ,"getRawVideo",{"accidentDetected":True}, False)

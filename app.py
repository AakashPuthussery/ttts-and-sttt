from flask import Flask, render_template, request, send_file
import pyttsx3
import speech_recognition as sr

app = Flask(__name__)

# Function to speak a message
def speak(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

# Function for speech recognition
def speech_recog():
    # Recognizer and Microphone are two classes inside the speech recognition module
    r = sr.Recognizer()
    mic = sr.Microphone()

    recognized_text = ""

    # Loop until the user decides to stop or audio is recognized
    while True:
        # Print and speak the message
        message = "Speak something or say 'stop' to end recording."
        speak(message)
        
        with mic as source:
            print("Listening...")
            # Listen function inside the speech recognition library
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                print("You said:", text)
                speak("You said: " + text)              
                recognized_text += text + "\n"

                # Check if the user wants to continue recording using audio
                if 'stop' in text.lower():
                    speak("Recording stopped.")
                    break  # Stop recording
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand that.")

    return recognized_text

# Route to handle text-to-speech conversion
@app.route('/text_to_speech_con', methods=['POST'])
def text_to_speech_con():
    text = request.form['text']
    text_speech = pyttsx3.init()
    text_speech.say(text)
    text_speech.runAndWait()
    return "Text converted to speech successfully."

# Route to handle speech-to-text recognition
@app.route('/speech_to_text_recog', methods=['GET'])
def speech_to_text_recog():
    recognized_text = speech_recog()
    return recognized_text

# Route to serve the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle download functionality
@app.route('/download', methods=['POST'])
def download():
    recognized_text = speech_recog()
    file_name = "recognized_text.txt"
    with open(file_name, 'w') as file:
        file.write(recognized_text)
    return send_file(file_name, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

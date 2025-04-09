from flask import Flask, render_template, request, jsonify, redirect, url_for
import face_recognition
import cv2
import numpy as np
import os
import time
import pyttsx3

app = Flask(__name__)

REGISTERED_FACES_DIR = os.path.join("Facedetection", "registered_faces")
known_face_encodings = []
known_face_names = {}

# Initialize text-to-speech engine


def speak(text):
    engine = pyttsx3.init()  # Create a new engine instance
    engine.say(text)
    engine.runAndWait()
    engine.stop()


# Ensure directory exists
if not os.path.exists(REGISTERED_FACES_DIR):
    os.makedirs(REGISTERED_FACES_DIR)

# Load registered faces
def load_registered_faces():
    global known_face_encodings, known_face_names
    known_face_encodings.clear()
    known_face_names.clear()

    for file in os.listdir(REGISTERED_FACES_DIR):
        if file.endswith(".npy"):
            username = file.split(".")[0]
            encoding = np.load(os.path.join(REGISTERED_FACES_DIR, file))
            known_face_encodings.append(encoding)
            known_face_names[username] = encoding

load_registered_faces()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/capture", methods=["POST"])
def capture():
    load_registered_faces()  # Reload known faces
    
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    time.sleep(0.2)

    ret, frame = cap.read()
    cap.release()

    if not ret:
        return jsonify({"message": "Failed to capture image!"})

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_frame)

    if not face_encodings:
        speak("No face detected!")
        return jsonify({"message": "No face detected!"})

    captured_encoding = face_encodings[0]
    matches = face_recognition.compare_faces(known_face_encodings, captured_encoding, tolerance=0.4)
    
    if True in matches:
        speak("Face detected successfully.")
        return jsonify({"redirect": "https://designeer1.github.io/main-site/"})  # Absolute URL for correct redirection
    else:
        speak("Face not recognized. Please register.")
        return jsonify({"register": True})

@app.route("/register", methods=["POST"])
def register():
    load_registered_faces()  # Reload known faces before registration
    
    data = request.get_json()
    username = data.get("username").strip()

    if not username:
        return jsonify({"message": "Username cannot be empty!"})

    if username in known_face_names:
        return jsonify({"message": "Username already exists! Try another name."})

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    time.sleep(0.2)

    ret, frame = cap.read()
    cap.release()

    if not ret:
        return jsonify({"message": "Failed to capture face!"})

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_frame)

    if not face_encodings:
        return jsonify({"message": "No face detected!"})

    new_encoding = face_encodings[0]

    for name, encoding in known_face_names.items():
        if face_recognition.compare_faces([encoding], new_encoding, tolerance=0.4)[0]:
            return jsonify({"message": f"Face already registered with username '{name}'!"})

    np.save(os.path.join(REGISTERED_FACES_DIR, f"{username}.npy"), new_encoding)
    load_registered_faces()
    speak("Face registered successfully!")
    
    return jsonify({"message": "Face registered successfully!", "redirect": url_for('home')})

@app.route("/login")
def login():
    return redirect("https://designeer1.github.io/main-site/")

if __name__ == "__main__":
    app.run(debug=True)



from flask import Flask, render_template, request, jsonify, redirect, url_for
from deepface import DeepFace
import cv2
import os
import time
import pyttsx3

app = Flask(__name__)

REGISTERED_FACES_DIR = os.path.join("Facedetection", "registered_faces")
if not os.path.exists(REGISTERED_FACES_DIR):
    os.makedirs(REGISTERED_FACES_DIR)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/capture", methods=["POST"])
def capture():
    cap = cv2.VideoCapture(0)
    time.sleep(0.2)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return jsonify({"message": "Failed to capture image!"})

    temp_path = os.path.join(REGISTERED_FACES_DIR, "temp.jpg")
    cv2.imwrite(temp_path, frame)

    for file in os.listdir(REGISTERED_FACES_DIR):
        if file.endswith(".jpg") and file != "temp.jpg":
            ref_path = os.path.join(REGISTERED_FACES_DIR, file)
            result = DeepFace.verify(img1_path=temp_path, img2_path=ref_path, model_name='Facenet', enforce_detection=False)
            if result["verified"]:
                speak("Face detected successfully.")
                return jsonify({"redirect": "https://designeer1.github.io/main-site/"})

    speak("Face not recognized. Please register.")
    return jsonify({"register": True})

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username").strip()
    if not username:
        return jsonify({"message": "Username cannot be empty!"})

    user_file = os.path.join(REGISTERED_FACES_DIR, f"{username}.jpg")
    if os.path.exists(user_file):
        return jsonify({"message": "Username already exists! Try another name."})

    cap = cv2.VideoCapture(0)
    time.sleep(0.2)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return jsonify({"message": "Failed to capture face!"})

    cv2.imwrite(user_file, frame)
    speak("Face registered successfully!")
    return jsonify({"message": "Face registered successfully!", "redirect": url_for('home')})

@app.route("/login")
def login():
    return redirect("https://designeer1.github.io/main-site/")

if __name__ == "__main__":
    app.run(debug=True)




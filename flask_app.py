from flask import Flask, render_template, request, redirect, url_for
import cv2
from PIL import Image
import io
import speech_recognition as sr
import paho.mqtt.client as mqtt
import numpy as np
import base64
import threading
import time

app = Flask(__name__)

# MQTT Setup
MQTT_BROKER = "test.mosquitto.org"  # Or your broker address
MQTT_PORT = 1883
MQTT_TOPIC = "image_processing/data"
mqtt_received_messages = []

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    mqtt_received_messages.append(msg.payload.decode())

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

# Simulated MQTT Publisher
def mqtt_publisher():
    while True:
        client.publish(MQTT_TOPIC, "Sensor Data: " + str(time.time()))
        time.sleep(5)

publisher_thread = threading.Thread(target=mqtt_publisher)
publisher_thread.daemon = True
publisher_thread.start()

# Image Processing Functions
def process_image(image_data, process_type):
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if process_type == "grayscale":
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif process_type == "edges":
        img = cv2.Canny(img, 100, 200)
    elif process_type == "resize":
        img = cv2.resize(img, (200, 200))

    _, img_encoded = cv2.imencode('.png', img)
    return base64.b64encode(img_encoded).decode('utf-8')

# Speech Recognition Function
def transcribe_audio(audio_data):
    r = sr.Recognizer()
    try:
        audio = sr.AudioFile(io.BytesIO(audio_data))
        with audio as source:
            audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Speech recognition could not understand audio"
    except sr.RequestError as e:
        return "Could not request results from Google Speech Recognition service; {0}".format(e)

@app.route("/", methods=["GET", "POST"])
def index():
    processed_image = None
    transcription = None

    if request.method == "POST":
        if "image" in request.files:
            image_file = request.files["image"].read()
            process_type = request.form.get("process_type")
            processed_image = process_image(image_file, process_type)
        elif "audio" in request.files:
            audio_file = request.files["audio"].read()
            transcription = transcribe_audio(audio_file)

    return render_template("index.html", processed_image=processed_image, transcription=transcription, mqtt_messages=mqtt_received_messages)

if __name__ == "__main__":
    app.run(debug=True)


# Go to http://127.0.0.1:5000/
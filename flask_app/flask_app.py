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

"""
MQTT_BROKER: Defines the address of the MQTT broker. Here, it uses "test.mosquitto.org", a public MQTT broker.
MQTT_PORT: Sets the MQTT broker port. The default MQTT port is 1883 (for non-secure connections).
MQTT_TOPIC: Specifies the topic to which the client will publish and subscribe. In this case, "image_processing/data".
mqtt_received_messages: Initializes an empty list to store messages received from the broker.
"""

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

"""
This function is called when the client successfully connects to the MQTT broker.
rc (result code) indicates the connection status (0 = success).
client.subscribe(MQTT_TOPIC): Subscribes the client to the specified topic ("image_processing/data") to receive messages.
"""

def on_message(client, userdata, msg):
    mqtt_received_messages.append(msg.payload.decode())

"""
This function is triggered whenever a new message arrives on the subscribed topic.
msg.payload.decode(): Decodes the message from bytes to a string.
The decoded message is appended to mqtt_received_messages.
"""

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

"""
mqtt.Client(): Creates an MQTT client instance.
client.on_connect = on_connect: Assigns the on_connect callback function to handle connection events.
client.on_message = on_message: Assigns the on_message callback function to process incoming messages.
"""

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

"""
client.connect(MQTT_BROKER, MQTT_PORT, 60): Connects to the MQTT broker on the given port. 
The 60 parameter is the keep-alive interval in seconds.
client.loop_start(): Starts a non-blocking loop to continuously handle network events and receive messages in the background.
"""

# Simulated MQTT Publisher
def mqtt_publisher():
    while True:
        client.publish(MQTT_TOPIC, "Sensor Data: " + str(time.time()))
        time.sleep(5)

"""
This function continuously publishes messages to the MQTT topic.
client.publish(MQTT_TOPIC, "Sensor Data: " + str(time.time())):
Sends a message with simulated sensor data (a timestamp).
time.sleep(5): Waits 5 seconds before sending the next message.
"""

publisher_thread = threading.Thread(target=mqtt_publisher)
publisher_thread.daemon = True
publisher_thread.start()

"""
threading.Thread(target=mqtt_publisher): Creates a new thread to run the mqtt_publisher() function.
publisher_thread.daemon = True: Ensures the thread terminates when the main program exits.
publisher_thread.start(): Starts the publisher thread.
"""

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
import tensorflow as tf
import tf_keras as keras
import os
import numpy as np
import pandas as pd
import tensorflow_hub as hub
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

UPLOAD_FOLDER = "./uploaded_images"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load labels
import os
labels_csv = pd.read_csv(os.path.join("data", "labels.csv"))
labels = labels_csv["breed"].to_numpy()
unique_breeds = np.unique(labels)

IMG_SIZE = 224
BATCH_SIZE = 32

# Function to preprocess image
def process_image(image_path):
    image = tf.io.read_file(image_path)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = tf.image.resize(image, size=[IMG_SIZE, IMG_SIZE])
    return image

# Function to load model
def load_model(model_path):
    print(f"Loading saved model from: {model_path}")
    return keras.models.load_model(model_path, custom_objects={"KerasLayer": hub.KerasLayer})

# Load trained model
model_path = "./20250327-07461743061579_full_image_set_mobilenetv2_Adam.h5"
loaded_model = load_model(model_path)

# Function to predict labels
def get_pred_label(prediction_probabilities):
    return unique_breeds[np.argmax(prediction_probabilities)]

@app.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    # Preprocess and predict
    image = process_image(file_path)
    image = tf.expand_dims(image, axis=0)  # Model expects a batch

    predictions = loaded_model.predict(image)
    predicted_label = get_pred_label(predictions[0])

    return jsonify({"prediction": predicted_label, "filename": filename})

@app.route("/")
def home():
    return "Flask Server Running on Render"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

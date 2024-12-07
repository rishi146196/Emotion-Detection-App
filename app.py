from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

# Initialize Flask app
app = Flask(__name__)

# Load the trained model
model = load_model("emtions.h5")

# Define class labels (adjust as per your model's output classes)
class_labels = ['surprised','sad','neutral','happy','fearful','disgusted','angry']  # Update with your emotion classes

@app.route('/')
def home():
    return render_template('index.html')  # HTML file for user upload interface

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded!"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected!"}), 400

    # Save uploaded image
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)

    # Preprocess the image (adjust preprocessing as per your model's input format)
    img = image.load_img(file_path, target_size=(224, 224))  # Adjust target size as per your model
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = img_array / 255.0  # Normalize if required

    # Predict emotion
    predictions = model.predict(img_array)
    predicted_class = class_labels[np.argmax(predictions)]

    return jsonify({"emotion": predicted_class})

if __name__ == "__main__":
    # Create uploads folder if not exists
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)

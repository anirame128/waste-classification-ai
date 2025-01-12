from flask import Flask, request, jsonify
import os
import tempfile
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import logging
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

# Load trained model
model = load_model("waste_classified_epoch_10_val_accuracy_0.94.h5")

# Class names must match the model's training
class_names = [
    "battery", "biological", "brown-glass", "cardboard", "clothes",
    "green-glass", "metal", "paper", "plastic", "shoes", "trash", "white-glass"
]

@app.route("/classify", methods=["POST"])
def classify_image():
    logging.info("Received a classification request.")

    # Validate file presence
    if "file" not in request.files or not request.files["file"].filename:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    # Validate file type (optional but recommended)
    if not file.content_type.startswith("image/"):
        return jsonify({"error": "Uploaded file is not an image"}), 400

    try:
        # Use a temporary file to handle the uploaded image
        with tempfile.NamedTemporaryFile(delete=True) as temp:
            file.save(temp.name)

            # Preprocess image
            img = image.load_img(temp.name, target_size=(224, 224))
            img_array = image.img_to_array(img) / 255.0  # Normalize to [0, 1]
            img_array = np.expand_dims(img_array, axis=0)

            # Predict using the trained model
            predictions = np.squeeze(model.predict(img_array))
            result = [
                {"label": class_names[i], "confidence": float(predictions[i])}
                for i in range(len(class_names))
            ]

            # Sort by confidence
            result = sorted(result, key=lambda x: x["confidence"], reverse=True)
            logging.info(f"Prediction result: {result}")
            return jsonify({"predictions": result})

    except Exception as e:
        logging.error(f"Error during classification: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

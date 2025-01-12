# Waste Classification AI

This project is an AI-powered waste classification system designed to identify types of waste using image classification. The system includes a trained model, a Flask backend API for classification, and a React Native frontend for uploading or capturing images for classification. The model was trained using TensorFlow and deployed locally for demonstration purposes.

---

## Features

- **Image Classification**: Classifies waste into 12 categories:
  - Battery
  - Biological
  - Brown-glass
  - Cardboard
  - Clothes
  - Green-glass
  - Metal
  - Paper
  - Plastic
  - Shoes
  - Trash
  - White-glass

- **Mobile App**:
  - Upload images from the gallery.
  - Capture images using the device camera.
  - Displays the top classification result with the highest confidence score.

- **Backend**:
  - Flask API for classification.
  - TensorFlow model integration.
  - Handles image preprocessing and prediction.

---

## Tech Stack

### Frontend
- React Native (Expo)
- Expo Image Picker for gallery and camera access

### Backend
- Flask
- TensorFlow
- Flask-CORS

### Deployment
- Local deployment for demo purposes
- Railway (optional for hosting the Flask backend)

---

## Installation and Setup

### Prerequisites

- Node.js and npm installed
- Python 3.9+
- Expo CLI installed globally:
  ```bash
  npm install -g expo-cli
  ```
- Install Python dependencies:
  ```bash
  pip install -r requirements.txt
  ```

---

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/waste-classification
   cd waste-classification/backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask API locally:
   ```bash
   python app.py
   ```

4. Test the API using Postman or curl:
   ```bash
   curl -X POST -F file=@image.jpg http://127.0.0.1:5000/classify
   ```

---

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the Expo server:
   ```bash
   expo start
   ```

4. Scan the QR code using the **Expo Go** app on your iPhone to view the app.

---

## Usage

1. Open the React Native app on your iPhone using Expo Go.
2. Select an image from the gallery or take a picture.
3. Press the "Classify Image" button.
4. View the classification result, showing the type of waste with the highest confidence score.

---

## Model Information

- **Architecture**: MobileNetV2 pretrained on ImageNet with custom classification layers.
- **Training Data**: Kaggle Garbage Classification dataset.
- **Output**: Trained TensorFlow model (`waste_classified_epoch_10_val_accuracy_0.94.h5`).

---

## Known Issues

- Misclassifications may occur due to insufficient training data for certain categories.
- Aluminum cans may be classified as plastic due to dataset limitations.
- Requires local Flask backend for the React Native app to work.

---

## Improvements and Future Work

1. **Dataset Expansion**:
   - Include more samples for underrepresented categories (e.g., aluminum cans).
2. **Model Optimization**:
   - Fine-tune the model with additional epochs and data augmentation.
3. **Deployment**:
   - Host the backend on a cloud platform like Railway or AWS.
   - Build and deploy the React Native app using Expo EAS for a standalone iOS app.

---

## Folder Structure

```
waste-classification/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── waste_classified_epoch_10_val_accuracy_0.94.h5
├── frontend/
│   ├── App.js
│   ├── package.json
│   ├── node_modules/
├── README.md
```

---

## License

This project is licensed under the MIT License.


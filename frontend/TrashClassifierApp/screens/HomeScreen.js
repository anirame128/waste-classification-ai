import React, { useState } from "react";
import { View, Text, Button, Image, StyleSheet, ActivityIndicator, Alert } from "react-native";
import * as ImagePicker from "expo-image-picker";

export default function HomeScreen() {
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [topResult, setTopResult] = useState(null);

  // Pick an image from the gallery
  const pickImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });

    if (!result.canceled) {
      setImage(result.assets[0].uri);
    }
  };

  // Take a picture using the camera
  const takePicture = async () => {
    const permission = await ImagePicker.requestCameraPermissionsAsync();
    if (!permission.granted) {
      Alert.alert("Permission Denied", "Camera permission is required to take pictures.");
      return;
    }

    const result = await ImagePicker.launchCameraAsync({
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });

    if (!result.canceled) {
      setImage(result.assets[0].uri);
    }
  };

  // Upload and classify the image
  const classifyImage = async () => {
    if (!image) {
      Alert.alert("No image selected", "Please select or take an image to classify.");
      return;
    }

    setLoading(true);
    try {
      // Prepare the form data
      const formData = new FormData();
      formData.append("file", {
        uri: image,
        name: "image.jpg",
        type: "image/jpeg",
      });

      // Send the POST request to the correct URL
      const response = await fetch(
        "https://waste-classification-ai-production.up.railway.app/classify",
        {
          method: "POST",
          headers: {
            "Content-Type": "multipart/form-data",
          },
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("API Response:", data);

      // The API returns a sorted list, so the first item has the highest confidence
      if (data && data.predictions && data.predictions.length > 0) {
        setTopResult(data.predictions[0]); // Save only the top result
      } else {
        Alert.alert("Error", "Unexpected response format from the server");
      }
    } catch (error) {
      console.error("Error classifying image:", error);
      Alert.alert("Error", "Failed to classify image. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Waste Classification</Text>
      {image && <Image source={{ uri: image }} style={styles.image} />}
      <Button title="Pick an Image" onPress={pickImage} />
      <Button title="Take a Picture" onPress={takePicture} />
      <Button title="Classify Image" onPress={classifyImage} />
      {loading && <ActivityIndicator size="large" color="#0000ff" />}
      {topResult && (
        <View style={styles.resultsContainer}>
          <Text style={styles.resultsTitle}>Top Classification Result:</Text>
          <Text style={styles.resultText}>
            {`${topResult.label}: ${(topResult.confidence * 100).toFixed(2)}%`}
          </Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    padding: 16,
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 16,
  },
  image: {
    width: 200,
    height: 200,
    marginBottom: 16,
  },
  resultsContainer: {
    marginTop: 16,
    alignItems: "center",
  },
  resultsTitle: {
    fontSize: 18,
    fontWeight: "bold",
    marginBottom: 8,
  },
  resultText: {
    fontSize: 16,
  },
});

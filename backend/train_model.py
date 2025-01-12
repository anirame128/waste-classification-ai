import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.callbacks import ModelCheckpoint
import os

# Dataset path
dataset_dir = "./garbage_classification"
model_save_path = "waste_classified_best.h5"  # Save the best model

# Parameters
img_height, img_width = 224, 224
batch_size = 32
epochs = 10

# Load raw datasets and extract class names
raw_train_dataset = tf.keras.utils.image_dataset_from_directory(
    dataset_dir,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size
)

raw_val_dataset = tf.keras.utils.image_dataset_from_directory(
    dataset_dir,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size
)

# Extract class names
class_names = raw_train_dataset.class_names
print(f"Class names: {class_names}")

# Prefetch data
AUTOTUNE = tf.data.AUTOTUNE

def normalize(image, label):
    image = tf.cast(image, tf.float32) / 255.0
    return image, label

train_dataset = raw_train_dataset.map(normalize).prefetch(buffer_size=AUTOTUNE)
val_dataset = raw_val_dataset.map(normalize).prefetch(buffer_size=AUTOTUNE)

# Load MobileNetV2
base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(img_height, img_width, 3))

# Add custom layers
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation="relu")(x)
predictions = Dense(len(class_names), activation="softmax")(x)
model = Model(inputs=base_model.input, outputs=predictions)

# Unfreeze last few layers
for layer in base_model.layers[-20:]:
    layer.trainable = True

# Compile model
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])

# Add ModelCheckpoint callback
checkpoint_callback = ModelCheckpoint(
    filepath="waste_classified_epoch_{epoch:02d}_val_accuracy_{val_accuracy:.2f}.h5",  # Save with epoch and val_accuracy in filename
    monitor="val_accuracy",  # Monitor validation accuracy
    save_best_only=True,  # Save only the best model
    save_weights_only=False,  # Save the full model
    verbose=1  # Print saving progress
)

# Train model with checkpoint callback
history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=epochs,
    callbacks=[checkpoint_callback]
)

# Save the final model
model.save(model_save_path)
print(f"Final model saved to {model_save_path}")

# Evaluate model
val_loss, val_accuracy = model.evaluate(val_dataset)
print(f"Validation Accuracy: {val_accuracy}")

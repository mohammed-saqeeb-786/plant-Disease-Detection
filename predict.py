import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

model = tf.keras.models.load_model("model.h5")

classes = ["Healthy", "Powdery", "Rust"]

def predict_image(img_path):
    try:
        img = image.load_img(img_path, target_size=(224,224))
        img = image.img_to_array(img) / 255.0
        img = np.expand_dims(img, axis=0)

        prediction = model.predict(img, verbose=0)

        class_index = np.argmax(prediction)
        label = classes[class_index]
        confidence = float(np.max(prediction)) * 100

        return {
            "title": label,
            "confidence": round(confidence, 2)
        }

    except Exception as e:
        return {"error": str(e)}
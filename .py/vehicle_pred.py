from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

# Load the saved model
model = load_model('vehicle_detection_model.h5')

# Function to predict if an image contains a vehicle
def predictvehicle(img_path):
    img = image.load_img(img_path, target_size=(64, 64))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    prediction = model.predict(img_array)
    result = prediction[0][0]
    if result > 0.8:
        print("The image contains a vehicle!",result)
        return "The image contains a vehicle!"
    else:
        print("The image does not contain a vehicle.")


# Test the model with an image
# img_path = 'C:\\Users\\User\\Downloads\\vehicle_detection\\dataset\\train\\vehicles\\3.png'  # Replace with your image path
# predict_image(img_path)
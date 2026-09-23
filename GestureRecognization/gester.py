# %% [markdown]
# ### Step1: Setup and import
# 

# %%
import subprocess
import sys

#install packages
packages = ['mediapipe','opencv-python','numpy','scikit-learn']

for package in packages:
    subprocess.check_
    call([sys.executable, "-m","pip","install",package, "-q"])
print("ALl packages installed successfully")

# %%
import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks import python
import numpy as np
import math
import time
import os
import urllib.request
from pathlib import Path
import matplotlib.pyplot as plt
from IPython.display import Image, display
print("ALl library imported successfully")
print(f"MediaPipe version {mp.__version__}")
print(f"CV2 version {cv2.__version__}")

# %% [markdown]
# ### Step 2: Download mediapipe models

# %%
# MODEL_DIR = os.path.expanduser("~/home/pratistha/mediapipe")
MODEL_DIR = os.path.expanduser("~/mediapipe")
os.makedirs(MODEL_DIR, exist_ok= True)
# URLs for the models
HAND_LANDMARKER_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task"
GESTURE_RECOGNIZER_URL = "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/latest/gesture_recognizer.task"

#define path to save model
HAND_LANDMARKER_PATH= os.path.join(MODEL_DIR, "hand_landmarker.task")
GESTURE_RECOGNIZER_PATH= os.path.join(MODEL_DIR, "gesture_recognizer.task")

print("Model path defined")
print(f"Model dir: {MODEL_DIR}")

# %%
## function to download model

import os
import urllib.request

def download_model(model_url, model_path, model_name):

    # check if file exists
    if os.path.exists(model_path):
        print(f"{model_name} already exists at {model_path}")
        return model_path

    print(f"Downloading {model_name}...")

    try:
        def progress_hook(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = min(int(downloaded * 100 / total_size), 100)
            print(f"\rProgress: {percent}%", end="")

        urllib.request.urlretrieve(
            model_url,
            model_path,
            progress_hook
        )

        print("\nDownload completed successfully!")

        return model_path

    except Exception as e:
        print("Error:", e)
        return None
print("Function created successfully")

# %%
## download model
print("Downloading models.....")
hand_model_path = download_model(
    HAND_LANDMARKER_URL,
    HAND_LANDMARKER_PATH,
    "Hand landmarker Model"
)
print(hand_model_path)
gesture_model_path = download_model(
    GESTURE_RECOGNIZER_URL,
    GESTURE_RECOGNIZER_PATH,
    "Gesture landmarker Model"
)

if hand_model_path and gesture_model_path:
    print("Model is ready to go....")
else:
    print("Failed to download")

# %% [markdown]
# ### Step 3: INITIALIZE PIPLELINE

# %%

hand_options = vision.HandLandmarkerOptions(
    base_options= python.BaseOptions(
        model_asset_path = hand_model_path
    ),
    num_hands=2,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.5,
    
)

hand_landmarker = vision.HandLandmarker.create_from_options(hand_options)
print("Hand landmarker initialized successfully")


# %%
# create a gesture recognizer

gesture_options = vision.GestureRecognizerOptions(
    base_options= python.BaseOptions(
        model_asset_path = gesture_model_path
    ),
    num_hands=2,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.5,
    
)

gesture_recognizer = vision.GestureRecognizer.create_from_options(gesture_options)
print("Gesture recognizer initialized successfully")

# %%
### Undestanding hand landmarks
# 21 points in one hand
landmark_info = {
    0: "Wrist (Center of hand)",
    4: "Thumb - TIP",
    8: "Index - TIP",
    12: "Middle - TIP",
    16: "Ring - TIP",
    20: "Pinky - TIP"
}
print("Import landmark")
for idx , name in landmark_info.items():
    print(f"Landmark {idx:2d}:{name}")

# %%
#create test image for hand
# STEP 5.1: Create a sample image
# In real usage, you'd load an actual hand photo

# Create a blank image (white background)
test_image = np.ones((400, 500, 3), dtype=np.uint8) * 255

# Draw a simple hand shape (for demonstration)
# Palm - circle in center
cv2.circle(test_image, (250, 200), 60, (200, 150, 100), -1)

# Fingers - lines from palm
cv2.line(test_image, (220, 140), (210, 50), (200, 150, 100), 20)   # Thumb
cv2.line(test_image, (250, 130), (250, 30), (200, 150, 100), 20)   # Index
cv2.line(test_image, (280, 140), (290, 50), (200, 150, 100), 20)   # Middle
cv2.line(test_image, (310, 150), (320, 80), (200, 150, 100), 20)   # Ring
cv2.line(test_image, (320, 180), (330, 130), (200, 150, 100), 20)  # Pinky

# Save and display
test_image_path = "test_hand_image.jpg"
cv2.imwrite(test_image_path, test_image)

print(f"✓ Test image created: {test_image.shape}")
print(f"  Size: 500×400 pixels")
print(f"  Saved as: {test_image_path}")

# Display
plt.figure(figsize=(6, 4))
plt.imshow(cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB))
plt.title("Test Hand Image")
plt.axis('off')
plt.tight_layout()
plt.show()

# %%
## import real hand image and identify landmark
hand= cv2.imread("hand-one.jpg")

## now convert BGR to RGB
rgb_img = cv2.cvtColor(hand,cv2.COLOR_BGR2RGB)

##Create media pipleline object
mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data = rgb_img)

## detect landmark 
hand_detection = hand_landmarker.detect(mp_img)
print("Detection successful")


# %%
### analyze detected landmarks
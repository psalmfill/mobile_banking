from google.cloud import vision
from google.cloud.vision_v1 import types
import io
import base64
import numpy as np

def verify_face(registered_photo_path, login_photo_data):
    client = vision.ImageAnnotatorClient()

    # Load the registered photo
    with open(registered_photo_path, 'rb') as image_file:
        registered_image = image_file.read()
    registered_face = types.Image(content=registered_image)

    # Load the login photo from base64 data
    try:
        login_image_data = base64.b64decode(login_photo_data.split(',')[1])  # Validate base64 encoding
    except (ValueError, IndexError):
        print("Error: Invalid base64 encoded login photo data")
        return False
    login_image = io.BytesIO(login_image_data)
    login_face = types.Image(content=login_image.read())

    # Detect faces and landmarks in both images
    try:
        registered_response = client.face_detection(image=registered_face)
        login_response = client.face_detection(image=login_face)
    except Exception as e:
        print(f"Error: An error occurred during API call: {e}")
        return False

    registered_faces = registered_response.face_annotations
    login_faces = login_response.face_annotations

    # Check if faces are detected in both images
    if len(registered_faces) > 0 and len(login_faces) > 0:
        registered_face = registered_faces[0]
        login_face = login_faces[0]

        # Compare facial landmarks
        registered_landmarks = extract_landmarks(registered_face)
        login_landmarks = extract_landmarks(login_face)

        # Calculate the Euclidean distance between corresponding landmarks
        if compare_landmarks(registered_landmarks, login_landmarks):
            return True

    return False

def extract_landmarks(face_annotation):
    """Extracts facial landmarks from a face annotation."""
    landmarks = {}
    for landmark in face_annotation.landmarks:
        landmarks[landmark.type_] = (landmark.position.x, landmark.position.y)
    return landmarks

def compare_landmarks(landmarks1, landmarks2, threshold=0.05):
    """Compares two sets of facial landmarks to determine if they match."""
    total_distance = 0
    count = 0

    for key in landmarks1.keys():
        if key in landmarks2:
            x1, y1 = landmarks1[key]
            x2, y2 = landmarks2[key]
            distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            total_distance += distance
            count += 1

    # Average distance per landmark
    avg_distance = total_distance / count if count > 0 else float('inf')

    # Compare average distance to threshold
    return avg_distance <= threshold

import cv2
import os
from deepface import DeepFace
import numpy as np

KNOWN_FACES_DIR = "faces"

# Load and encode known faces
known_encodings = []
known_names = []

for file in os.listdir(KNOWN_FACES_DIR):
    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
        file_path = f"{KNOWN_FACES_DIR}/{file}"
        try:
            # Extract face embedding using DeepFace
            result = DeepFace.represent(img_path=file_path, model_name='Facenet')
            if result:
                known_encodings.append(result[0]['embedding'])
                known_names.append(file.split(".")[0])
        except Exception as e:
            print(f"⚠️ Error processing {file}: {e}")

def verify_face(current_embedding, threshold=0.6):
    """Compare current face embedding with known faces"""
    for known_embedding, known_name in zip(known_encodings, known_names):
        distance = np.linalg.norm(np.array(current_embedding) - np.array(known_embedding))
        if distance < threshold:
            return True, known_name
    return False, None

def process_frame(frame, threshold=0.6):
    """Process a single frame to detect and verify faces"""
    try:
        results = DeepFace.extract_faces(img_path=frame, enforce_detection=False)
        
        if results:
            face_result = DeepFace.represent(img_path=frame, model_name='Facenet')
            if face_result:
                current_embedding = face_result[0]['embedding']
                verified, name = verify_face(current_embedding, threshold)
                if verified:
                    return True, name
        return False, None
    except Exception:
        return False, None

def authenticate_face(threshold=0.6):
    """Authenticate face using webcam"""
    video = cv2.VideoCapture(0)
    
    if not video.isOpened():
        print("❌ Cannot open webcam")
        return False

    print("🔐 Face Authentication Started...")
    print("Press 'q' to quit")

    while True:
        ret, frame = video.read()
        if not ret:
            print("❌ Failed to read frame")
            break

        verified, name = process_frame(frame, threshold)
        if verified:
            print(f"✅ Face Verified - {name}")
            video.release()
            cv2.destroyAllWindows()
            return True
        
        cv2.imshow("FERRDY Face Auth", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
    return False

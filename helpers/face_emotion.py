from deepface import DeepFace
import cv2
from collections import Counter

def detect_emotion(video_path):
    cap = cv2.VideoCapture(video_path)
    emotions = []
    i = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        if i % 30 == 0:
            try:
                res = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
                emotions.append(res[0]['dominant_emotion'])
            except:
                continue
        i += 1
    cap.release()
    return Counter(emotions).most_common(1)[0][0] if emotions else "Unknown"

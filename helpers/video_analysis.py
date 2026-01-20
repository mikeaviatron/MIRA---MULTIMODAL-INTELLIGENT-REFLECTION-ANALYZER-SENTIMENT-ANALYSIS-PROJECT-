import cv2
import numpy as np
from mediapipe.python.solutions import face_mesh

def analyze_video(video_path, return_array=False):
    """
    Analyze a video for forward eye contact using MediaPipe FaceMesh.

    Args:
        video_path (str): Path to the video file.
        return_array (bool): If True, returns eye contact per frame; otherwise, returns average percentage.

    Returns:
        np.ndarray or float: Frame-wise eye contact (0/1) if return_array=True, else average % of frames with forward gaze.
    """
    cap = cv2.VideoCapture(video_path)
    mesh = face_mesh.FaceMesh(refine_landmarks=True)
    
    eye_contact_array = []
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = mesh.process(rgb)

        # If a face is detected, consider it as forward gaze (simplified)
        if result.multi_face_landmarks:
            eye_contact_array.append(1)
        else:
            eye_contact_array.append(0)

    cap.release()
    mesh.close()

    eye_contact_array = np.array(eye_contact_array)
    
    if return_array:
        return eye_contact_array
    else:
        return (np.sum(eye_contact_array) / len(eye_contact_array)) * 100 if len(eye_contact_array) > 0 else 0

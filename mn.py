import cv2
import mediapipe as mp
import random
import time

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

def get_heart_rate():
    return random.randint(60, 100)

def check_posture(landmarks):
    feedback = []
    
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    shoulder_diff = abs(left_shoulder.y - right_shoulder.y)
    if shoulder_diff > 0.05:
        feedback.append("Adjust your shoulders to be level.")
    return feedback

cap = cv2.VideoCapture(0)

print("Starting camera. Press 'q' to exit.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty frame.")
        continue

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.pro
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        landmarks = results.pose_landmarks.landmark
        feedback = check_posture(landmarks)

        for i, text in enumerate(feedback):
            cv2.putText(frame, text, (10, 30 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

    heart_rate = get_heart_rate()
    cv2.putText(frame, f"Heart Rate: {heart_rate} bpm", (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('Fitness Tracker', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
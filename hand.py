import cv2
import mediapipe as mp
import numpy as np
import streamlit as st


click_count = 0
click_threshold = 10  # Adjust this threshold for a click gesture

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

def hand_gesture_recognition():
    global click_count

    # Open webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect hand landmarks
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # คัดแยกจุดสำหรับนิ้วโป้งและนิ้วชี้
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                # คำนวณระยะห่างระหว่างจุดสำหรับนิ้วโป้งและนิ้วชี้
                distance = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5

                # If the distance is below a threshold, increment click count
                if distance < 0.05:  # Adjust this threshold based on your hand movements
                    click_count += 1

        # แสดง count ใน Streamlit
        st.write(f"Air Mouse Clicks: {click_count}")

        # แสดง video ใน Streamlit
        st.image(frame, channels="BGR", use_column_width=True)

        # ปิดโปรแกรมเมื่อกด ESC
        if cv2.waitKey(1) == 27:
            break

    # Release the camera
    cap.release()
    cv2.destroyAllWindows()

# Streamlit UI
st.title("Hand Gesture Recognition and Click Counter")
st.write("Use hand gestures to simulate clicks")

# Run hand gesture recognition and counting when the Streamlit app starts
hand_gesture_recognition()

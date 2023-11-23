import mediapipe as mp
import numpy as np
import cv2
import subprocess
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer
import av

# Initialize MediaPipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Function to set volume using subprocess
def set_volume(volume):
    subprocess.run(["osascript", "-e", f"set volume output volume {volume}"])

def process_video_frame(image):
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    volume = 50  # Initial volume level
    pinch_threshold = 0.05  # Threshold to differentiate touch from apart

    if results.multi_hand_landmarks:
        # Assume only one hand in the frame for simplicity
        hand_landmarks = results.multi_hand_landmarks[0]

        # Get landmarks for thumb and index finger
        thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        thumb_x, thumb_y = thumb_tip.x, thumb_tip.y
        index_x, index_y = index_tip.x, index_tip.y

        # Calculate distance between thumb and index finger landmarks
        distance = ((thumb_x - index_x) ** 2 + (thumb_y - index_y) ** 2) ** 0.5

        # Get landmarks for additional fingers
        middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

        # Check for hand gesture to increase volume (open hand)
        if (
            thumb_y < middle_tip.y < ring_tip.y < pinky_tip.y and
            thumb_x < index_x and distance > pinch_threshold
        ):
            volume += 1 if volume < 100 else 0  # Increase volume when open hand detected

        # Check for hand gesture to decrease volume (closed hand)
        elif (
            thumb_y > index_y and thumb_x < index_x and distance < pinch_threshold
        ):
            volume -= 1 if volume > 0 else 0  # Decrease volume when closed hand (fist) detected

        set_volume(volume)  # Set the adjusted volume level

        # Draw hand landmarks and skeleton on the image
        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Display current volume level in the frame
        cv2.putText(image, f"Volume: {volume}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    return image

def video_frame_callback(frame):
    image = frame.to_ndarray(format="bgr24")
    processed_image = process_video_frame(image)
    return av.VideoFrame.from_ndarray(processed_image, format="bgr24")

def result_page():
    st.title("Hand Gesture Volume Control - Result")
    st.write("Enable the hand gesture recognition to control the volume.")
    st.write("Click the button below to start recognizing hand gestures for volume control.")

    webrtc_streamer(
        key="hand_gesture_volume_control", 
        mode=WebRtcMode.SENDRECV,
        video_frame_callback=video_frame_callback,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
        rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        }
    )

result_page()

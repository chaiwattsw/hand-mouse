import mediapipe as mp
import cv2
import subprocess
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer
import av

st.set_page_config(page_title="Result")

# Initialize MediaPipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Function to set volume using subprocess
def set_volume(volume):
    subprocess.run(["osascript", "-e", f"set volume output volume {volume}"])

# Hand gesture recognition and volume control
def video_frame_callback(frame):
    image = frame.to_ndarray(format="bgr24")
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    current_volume = 50  # Initialize with a default volume value

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get finger landmarks
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_x, thumb_y = thumb_tip.x, thumb_tip.y
            index_x, index_y = index_tip.x, index_tip.y

            # Calculate distance between thumb and index finger landmarks
            distance = ((thumb_x - index_x) ** 2 + (thumb_y - index_y) ** 2) ** 0.5
            pinch_threshold = 0.05  # Threshold to differentiate touch from apart

            # Adjust volume based on hand gesture
            if distance < pinch_threshold:
                current_volume -= 1 if current_volume > 0 else 0  # Decrease volume
            else:
                current_volume += 1 if current_volume < 100 else 0  # Increase volume

            # Set volume using subprocess
            set_volume(current_volume)

            # Display current volume level in the frame
            cv2.putText(image, f"Volume: {current_volume}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    return av.VideoFrame.from_ndarray(image, format="bgr24")

def result_page():
    st.title("Hand Gesture Volume Control - Result")
    st.write("Enable the hand gesture recognition to control the volume.")
    st.write("Click the button below to start recognizing hand gestures for volume control.")

    webrtc_streamer(
        key="hand_gesture_volume_control", 
        mode=WebRtcMode.SENDRECV,
        video_frame_callback=video_frame_callback,
        media_stream_constraints={"video": True, "audio": False},
        video_processor_factory=video_frame_callback,
        rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        },
        async_processing=True,
    )

result_page()

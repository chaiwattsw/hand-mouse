import mediapipe as mp
import cv2
import subprocess
import streamlit as st

st.set_page_config(page_title="Result")

# Initialize MediaPipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Function to set volume using subprocess
def set_volume(volume):
    subprocess.run(["osascript", "-e", f"set volume output volume {volume}"])

def result_page():
    st.title("Hand Gesture Volume Control - Result")
    st.write("Enable the hand gesture recognition to control the volume.")
    st.write("Click the button below to start recognizing hand gestures for volume control.")
    
    # Initialize volume outside the loop
    volume = 50  # Set an initial volume value

    # Create a button to start gesture recognition
    start_button = st.button("Start Gesture Recognition")

    # OpenCV video capture setup
    cap = cv2.VideoCapture(0)

    # Loop until the button is released
    while start_button:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the image to RGB and process it
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get finger landmarks
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_x, thumb_y = thumb_tip.x, thumb_tip.y
                index_x, index_y = index_tip.x, index_tip.y

                # Calculate distance between thumb and index finger landmarks
                distance = ((thumb_x - index_x) ** 2 + (thumb_y - index_y) ** 2) ** 0.5
                pinch_threshold = 0.05  # Threshold to differentiate touch from apart

                # Decrease volume if fingers touch, otherwise increase it
                if distance < pinch_threshold:
                    volume -= 1 if volume > 0 else 0  # Decrease volume
                else:
                    volume += 1 if volume < 100 else 0  # Increase volume

                # Set volume using subprocess
                set_volume(volume)

                # Debug information
                st.write(f"Distance: {distance}. Volume: {volume}")

        # Display the video feed with hand landmarks
        st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="BGR")

        # Display the current volume level
        st.write(f"Current Volume Level: {volume}")

    # Release resources when the button is not pressed
    cap.release()
    cv2.destroyAllWindows()

result_page()

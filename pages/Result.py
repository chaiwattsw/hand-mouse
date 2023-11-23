import mediapipe as mp
import numpy as np
import cv2
import streamlit as st
from streamlit_webrtc import (WebRtcMode, webrtc_streamer)
import av
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initialize MediaPipe hands module
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Volume Control Library Usage
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol, maxVol, volBar, volPer = volRange[0], volRange[1], 400, 0

# Function to control volume based on hand gestures
def control_volume(hand_landmarks):
    if hand_landmarks:
        myHand = hand_landmarks[0]
        lmList = []
        for id, lm in enumerate(myHand.landmark):
            h, w, c = image.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])

        if len(lmList) != 0:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]

            length = math.hypot(x2 - x1, y2 - y1)
            if length < 50:
                vol = np.interp(length, [50, 220], [minVol, maxVol])
                volume.SetMasterVolumeLevel(vol, None)
                volBar = np.interp(length, [50, 220], [400, 150])
                volPer = np.interp(length, [50, 220], [0, 100])

                # Display volume level and bar here using Streamlit components

# Streamlit application
def main():
    st.title("Hand Gesture Volume Control - Streamlit")
    st.write("Enable hand gesture recognition to control the volume.")
    st.write("Click the button below to start recognizing hand gestures.")

    webrtc_ctx = webrtc_streamer(
        key="hand_gesture_volume_control",
        mode=WebRtcMode.SENDRECV,
        async_processing=True,
    )

    if webrtc_ctx.video_receiver:
        while True:
            try:
                frame = webrtc_ctx.video_receiver.get_frame(timeout=1)
                if frame is None:
                    continue

                image = frame.to_ndarray(format="bgr24")
                with mp_hands.Hands(
                    model_complexity=0,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) as hands:
                    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

                    if results.multi_hand_landmarks:
                        control_volume(results.multi_hand_landmarks)
                    
                    # Display the image in Streamlit
                    st.image(image, channels="BGR")
            except av.VideoFrameTimeout:
                print("Timeout for video frame")

if __name__ == "__main__":
    main()

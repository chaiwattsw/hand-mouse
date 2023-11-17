import mediapipe as mp
import cv2
import subprocess
import streamlit as st

# Initialize MediaPipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Function to set volume using subprocess
def set_volume(volume):
    subprocess.run(["osascript", "-e", f"set volume output volume {volume}"])

# Create unique keys for the checkboxes
enable_gesture_recognition_key = "enable_gesture_recognition"
result_page_key = "result_page"

def information_page():
    st.title("Hand Gesture Volume Control")

    st.header("วัตถุประสงค์เพื่อศึกษา")
    st.write("1). พัฒนาตัวแบบระบบตรวจับนิ้วมือ เพื่อใช้ในการ ปรับค่าแสงหน้าจอแสดงผล")
    st.write("2). เพื่อหาประสิทธิภาพของ ตัวแบบระบบตรวจจับมือเรียนรู้ของเครื่องร่วมกับการตรวจจับ วัตถุ ข้อมูลที่ใช้ในการ เรียนรู้ของเครื่อง คือ โดยการจับจุดจากนิ้วมือเพื่อแสดงตำแหน่งแต่ละจุดของนิ้วมือ")

    st.header("เหตุผล")
    st.write("การจับกาหรือขยับมือเพื่อปรับแสงอาจมีเหตุผลหลายประการ เช่น")
    st.write("การปรับตัวกับแสง: เมื่อมีการเปลี่ยนแปลงของแสง เช่น แสงสว่างหรือแสงที่มืดลง เรามักจะปรับตัวเพื่อให้สามารถมองเห็นได้ชัดเจนมากขึ้น การจับกาหรือขยับมือในที่นี้อาจช่วยปรับตัวหรือปรับเปลี่ยนท่าทางของร่างกายเพื่อให้สามารถรับแสงได้อย่างเหมาะสมกับสภาพแวดล้อมที่มืดหรือสว่างขึ้น")
    st.write("การสื่อสารทางร่างกาย: การใช้การจับกาหรือขยับมือเพื่อปรับแสงอาจเป็นส่วนหนึ่งของการสื่อสารทางร่างกาย เช่น เมื่อมีแสงสว่างเข้มที่มาทันที การปิดดวงตาหรือการใช้มือบดบังแสงอาจเป็นการสื่อสารว่าสภาพแวดล้อมมีการเปลี่ยนแปลง")

    st.header("หลักการ")
    st.write("การขยับของนิ้วมือในการปรับแสงเกี่ยวข้องกับระบบการรับรู้แสงและการประมวลผลของสมองที่ทำให้มนุษย์สามารถปรับตัวต่อการเปลี่ยนแปลงของแสงได้ มีหลายประการที่เกี่ยวข้องกับหลักการนี้: การรับรู้แสงโดยตรง: นิ้วมือและมือมนุษย์มีความสามารถในการรับรู้แสง โดยการรับรู้การเปลี่ยนแปลงของแสงและเงื่อนไขแสงที่แตกต่างกัน เช่น การเข้าแสงจากแหล่งแสงต่าง ๆ การสว่างและมืด ซึ่งส่งผลให้นิ้วมือสามารถปรับตัวต่อเงื่อนไขแสงได้โดยการเปิดหรือปิดตัวของตัวรับรู้แสง เช่น ตาหรือผิวหนังที่ใช้ในการรับรู้แสง การปรับตัวต่อการเปลี่ยนแปลงของแสง: นิ้วมือสามารถเปลี่ยนแปลงการที่เป็นไปได้ต่อการเปลี่ยนแปลงของแสง เช่น การปรับมือเพื่อลดแสงที่มาจากแหล่งแสงสูง เพื่อป้องกันการเจ็บตาหรือการปรับตัวที่เกี่ยวข้องกับการเห็นในสภาพแสงที่แตกต่างกัน")

    st.header("ทฤษฏี")
    st.write("2.1 ปัญญาประดิษฐ์ (Artificial Intelligence) เป็นเทคโนโลยีที่จำลองความฉลาดของมนุษย์ โดยการพัฒนาระบบ อัจฉริยะที่มีความสามารถในการรับรู้ เรียนรู้ใช้เหตุผลและตัดสินใจเลือกทางเลือกที่ดีสุดจากการวิเคราะห์ข้อมูลที่ เกี่ยวข้องพิจารณาทางเลือกต่างๆ")
    st.write("2.2 Machine Learning หรือ การเรียนรู้ของเครื่อง เป็นสาขาหนึ่งของปัญญาประดิษฐ์ (Artificial Intelligence) การ ที่จะพัฒนาให้ระบบมีความฉลาด และความสามารถ ระบบจำเป็นที่จะต้องมีการเรียนรู้สถานการณ์ เพื่อที่จะได้วางแผนและ ตัดสินใจแก้ปัญหาได้เหมือนกับมนุษย์ ")
    st.write("2.3 การวิเคราะห์การถดถอยเชิงเส้น (Linear Regression) เป็น Machine Learning ประเภท Supervised Learning หรือ การเรียนรู้แบบมีผู้สอน ชนิดแบบ Statistical Regression ที่เราจะต้องใส่ชุดข้อมูลเข้าไปให้โปรแกรมเรียนรู้ ก่อน โดยโปรแกรมจะนำตัวแปรต้นและตัวแปรตามไปคำนวณด้วยสถิติทางคณิตศาสตร์ แล้วก็จะได้ข้อมูลกลับมาเป็นตัวเลข")

def result_page():
    st.title("Hand Gesture Volume Control - Result")
    st.write("Enable the hand gesture recognition to control the volume.")
    st.write("Click the button below to start recognizing hand gestures for volume control.")
    
    # Initialize volume outside the loop
    volume = 50  # Set an initial volume value

    # Display the current volume level
    st.write(f"Current Volume Level: {volume}")

    # OpenCV video capture setup
    cap = cv2.VideoCapture(0)

    while True:
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
                pinch_threshold = 0.05  # Example threshold

                if distance < pinch_threshold:
                    # Pinch gesture detected, adjust volume based on finger position
                    volume = int((1 - index_y) * 100)
                    set_volume(volume)

        # Display the video feed with hand landmarks
        st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="BGR")

        # Display the current volume level
        st.write(f"Current Volume Level: {volume}")


    # Release resources
    cap.release()
    cv2.destroyAllWindows()

def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Information", "Result"])

    if selection == "Information":
        information_page()
    elif selection == "Result":
        result_page()

if __name__ == "__main__":
    main()

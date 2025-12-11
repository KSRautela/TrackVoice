import cv2
import cv2.aruco as aruco
import serial
import time
import numpy as np

# === Serial setup ===
ser = serial.Serial('COM6', 115200)  # Change COM port if needed
time.sleep(2)

# === Video capture ===
cap = cv2.VideoCapture(1)
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, parameters)

# === Servo state tracking ===
prevX, prevY = -1, -1
smoothedX, smoothedY = 90, 90  # initial midpoint

# === Tuning parameters ===
SMOOTHING_FACTOR = 0.2  # 0 = no smoothing, 1 = instant snap
MIN_CHANGE = 1          # min degree change needed to send command

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_height, frame_width = frame.shape[:2]
    FRAME_CENTER_X = frame_width // 2
    FRAME_CENTER_Y = frame_height // 2

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = detector.detectMarkers(gray)

    command_text = ""

    if ids is not None:
        for corner in corners:
            int_corners = corner[0].astype(int)
            center_x = int(int_corners[:, 0].mean())
            center_y = int(int_corners[:, 1].mean())

            # Draw visuals
            cv2.polylines(frame, [int_corners], True, (0, 255, 0), 2)
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
            cv2.drawMarker(frame, (FRAME_CENTER_X, FRAME_CENTER_Y), (255, 0, 0), cv2.MARKER_CROSS, 20, 2)
            cv2.line(frame, (center_x, center_y), (FRAME_CENTER_X, FRAME_CENTER_Y), (255, 255, 0), 1)

            # === Map position to angle ===
            rawX = np.interp(center_x, [0, frame_width], [0, 180])     # pan
            rawY = np.interp(center_y, [0, frame_height], [0, 180])    # tilt

            # === Optional: flip X axis direction if needed ===
            # rawX = 180 - rawX  # uncomment if movement is reversed

            # === Smoothing ===
            smoothedX = smoothedX * (1 - SMOOTHING_FACTOR) + rawX * SMOOTHING_FACTOR
            smoothedY = smoothedY * (1 - SMOOTHING_FACTOR) + rawY * SMOOTHING_FACTOR

            intX = int(smoothedX)
            intY = int(smoothedY)

            # === Avoid repeating same command ===
            if abs(intX - prevX) >= MIN_CHANGE or abs(intY - prevY) >= MIN_CHANGE:
                command_text = f"X{intX} Y{intY}"
                ser.write((command_text + '\n').encode())
                prevX, prevY = intX, intY

    # Display command text
    if command_text:
        cv2.putText(frame, f"Sent: {command_text}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # Show window
    cv2.imshow("Aruco Tracker", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
ser.close()

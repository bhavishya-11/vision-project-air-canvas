import cv2
import numpy as np
import mediapipe as mp
from collections import deque
import tkinter as tk
from tkinter import messagebox
from threading import Thread

# Points for different colors
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

# Indexes to keep track of points for each color
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0

# Kernel for dilation
kernel = np.ones((5, 5), np.uint8)

# Colors: Blue, Green, Red, Yellow
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0

# Initialize MediaPipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Variables for drawing logic
drawing = False  # Drawing state (True when index finger is moving and thumb is not touching)
thumb_touching = False  # Flag to check if thumb and index finger are touching
running = False  # Flag to control the running state of the app

def start_drawing():
    global running
    running = True
    Thread(target=run_app).start()  # Start the app in a new thread

def stop_drawing():
    global running
    running = False

def run_app():
    global bpoints, gpoints, rpoints, ypoints
    global blue_index, green_index, red_index, yellow_index
    global colorIndex, drawing, thumb_touching
    
    # Set up canvas window
    paintWindow = np.zeros((471, 636, 3)) + 255
    paintWindow = cv2.rectangle(paintWindow, (40, 1), (140, 65), (0, 0, 0), 2)
    paintWindow = cv2.rectangle(paintWindow, (275, 1), (375, 65), colors[0], 2)
    paintWindow = cv2.rectangle(paintWindow, (160, 1), (255, 65), colors[1], 2)
    paintWindow = cv2.rectangle(paintWindow, (390, 1), (485, 65), colors[2], 2)
    paintWindow = cv2.rectangle(paintWindow, (505, 1), (600, 65), colors[3], 2)

    cv2.putText(paintWindow, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.namedWindow('Paint', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Output', cv2.WINDOW_NORMAL)

    # Webcam initialization
    cap = cv2.VideoCapture(0)

    while running:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip frame for mirror effect
        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Draw the UI buttons
        frame = cv2.rectangle(frame, (40, 1), (140, 65), (0, 0, 0), 2)  # CLEAR button
        frame = cv2.rectangle(frame, (160, 1), (255, 65), (255, 0, 0), 2)  # BLUE button
        frame = cv2.rectangle(frame, (275, 1), (375, 65), (0, 255, 0), 2)  # GREEN button
        frame = cv2.rectangle(frame, (390, 1), (485, 65), (0, 0, 255), 2)  # RED button
        frame = cv2.rectangle(frame, (505, 1), (600, 65), (0, 255, 255), 2)  # YELLOW button
        
        cv2.putText(frame, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

        # Process hand landmarks
        result = hands.process(framergb)

        # Check if landmarks are detected
        if result.multi_hand_landmarks:
            landmarks = []
            for handLms in result.multi_hand_landmarks:
                for lm in handLms.landmark:
                    lmx = int(lm.x * frame.shape[1])
                    lmy = int(lm.y * frame.shape[0])
                    landmarks.append((lmx, lmy))

                # Drawing the landmarks on the frame
                mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

            # Get thumb and index finger landmarks
            thumb_tip = landmarks[4]
            index_tip = landmarks[8]

            # Calculate distance between thumb and index finger
            distance = np.sqrt((thumb_tip[0] - index_tip[0]) ** 2 + (thumb_tip[1] - index_tip[1]) ** 2)

            # Stop drawing if thumb and index finger are touching
            if distance < 40:
                drawing = False
                thumb_touching = True
            else:
                thumb_touching = False

            # Detect if the clear button is pressed (top-left corner)
            if 40 <= index_tip[0] <= 140 and 1 <= index_tip[1] <= 65:
                # Clear the canvas by resetting points
                bpoints = [deque(maxlen=1024)]
                gpoints = [deque(maxlen=1024)]
                rpoints = [deque(maxlen=1024)]
                ypoints = [deque(maxlen=1024)]
                blue_index = green_index = red_index = yellow_index = 0
                paintWindow[67:, :, :] = 255

            # Detect if the BLUE button is pressed
            elif 160 <= index_tip[0] <= 255 and 1 <= index_tip[1] <= 65:
                colorIndex = 0  # Set color to BLUE

            # Detect if the GREEN button is pressed
            elif 275 <= index_tip[0] <= 375 and 1 <= index_tip[1] <= 65:
                colorIndex = 1  # Set color to GREEN

            # Detect if the RED button is pressed
            elif 390 <= index_tip[0] <= 485 and 1 <= index_tip[1] <= 65:
                colorIndex = 2  # Set color to RED

            # Detect if the YELLOW button is pressed
            elif 505 <= index_tip[0] <= 600 and 1 <= index_tip[1] <= 65:
                colorIndex = 3  # Set color to YELLOW

            # If thumb is not touching, allow drawing with index finger
            if not thumb_touching:
                drawing = True
                if colorIndex == 0:
                    bpoints[blue_index].appendleft(index_tip)
                elif colorIndex == 1:
                    gpoints[green_index].appendleft(index_tip)
                elif colorIndex == 2:
                    rpoints[red_index].appendleft(index_tip)
                elif colorIndex == 3:
                    ypoints[yellow_index].appendleft(index_tip)

        # Draw points on canvas for each color deque
        points = [bpoints, gpoints, rpoints, ypoints]
        for i in range(len(points)):
            for j in range(len(points[i])):
                for k in range(1, len(points[i][j])):
                    if points[i][j][k - 1] is None or points[i][j][k] is None:
                        continue
                    cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                    cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

        cv2.imshow("Output", frame)
        cv2.imshow("Paint", paintWindow)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Tkinter GUI
root = tk.Tk()
root.title("Air Canvas Controller")

start_button = tk.Button(root, text="START", command=start_drawing, height=2, width=10, bg="green")
stop_button = tk.Button(root, text="STOP", command=stop_drawing, height=2, width=10, bg="red")

start_button.pack(pady=10)
stop_button.pack(pady=10)

root.mainloop()
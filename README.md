# 🎨 Vision Air Canvas

Vision Air Canvas is a real-time computer vision project that allows users to draw in the air using their index finger via webcam. It utilizes **MediaPipe** for hand tracking and **OpenCV** for rendering the virtual canvas. No stylus, no touchscreen — just gestures and creativity!

---

## 📌 Features

- 🖐️ Finger gesture detection with MediaPipe
- 🎨 Real-time air drawing on virtual canvas
- 🖌️ Color selection (Blue, Green, Red, Yellow)
- 🧼 Clear screen gesture
- 🖥️ GUI control panel using Tkinter (Start/Stop)
- 💡 Interactive buttons drawn directly on the video feed

---

## 🛠️ Tech Stack

- **Python 3**
- **OpenCV**
- **MediaPipe**
- **NumPy**
- **Tkinter**

---

## 🚀 How It Works

1. **Hand Tracking**: MediaPipe detects the hand and tracks landmarks (especially index and thumb).
2. **Drawing Logic**:
   - **Index finger moves**: Start drawing.
   - **Thumb & Index touch**: Pause drawing.
3. **UI Buttons (Drawn on screen)**:
   - Select colors (Blue, Green, Red, Yellow)
   - Clear the canvas
4. **GUI Controller**: Tkinter window to Start/Stop the app.

---

## ▶️ How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/bhavishya-11/vision-air-canvas.git
   cd vision-air-canvas
## 👨‍💻 Authors

### 🧠 Bhavishya Chauhan  
- Final Year B.Tech in AI & ML  
- Loves to blend creativity with code  
- GitHub: [@bhavishya-11](https://github.com/bhavishya-11)

### 🧠 Jitendra Chaudhary 
- Final Year B.Tech in AI & ML  
- Passionate about computer vision and innovation  
- GitHub: [@jitendra0730](https://github.com/jitendra0730)

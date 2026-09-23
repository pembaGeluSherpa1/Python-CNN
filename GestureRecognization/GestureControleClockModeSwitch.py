import cv2
import mediapipe as mp
import tkinter as tk
from datetime import datetime
import math
import numpy as np
import threading
import os
import time
from PIL import Image, ImageTk

# Find or download the gesture_recognizer.task model file
model_path = None
possible_paths = [
    "gesture_recognizer.task",
    os.path.expanduser("~/mediapipe/gesture_recognizer.task"),
    "/Users/pembagelusherpa/Desktop/python_kritim/GestureRecognization/gesture_recognizer.task"
]

for p in possible_paths:
    if os.path.exists(p):
        model_path = p
        break

if model_path is None:
    print("gesture_recognizer.task not found locally. Downloading...")
    os.makedirs(os.path.expanduser("~/mediapipe"), exist_ok=True)
    url = "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/latest/gesture_recognizer.task"
    model_path = os.path.expanduser("~/mediapipe/gesture_recognizer.task")
    import urllib.request
    try:
        urllib.request.urlretrieve(url, model_path)
        print(f"Downloaded successfully to {model_path}")
    except Exception as e:
        print("Download failed! Please place gesture_recognizer.task in the current directory. Error:", e)
else:
    print(f"Using model from: {model_path}")


class GestureClockApp:
    def __init__(self, root, model_path):
        self.root = root
        self.model_path = model_path
        self.root.title("Gesture Clock Dashboard")
        self.root.geometry("820x500")
        self.root.configure(bg="#121212")
        self.root.resizable(False, False)
        
        # Application State
        self.mode = "analog"  # 'analog' or 'digital'
        self.last_gesture = "None"
        self.running = True
        self.latest_frame = None
        
        # Main Title
        title_label = tk.Label(
            self.root, 
            text="GESTURE CONTROLLED CLOCK", 
            font=("Helvetica", 18, "bold"), 
            fg="#00e5ff", 
            bg="#1e1e1e",
            pady=10
        )
        title_label.pack(fill=tk.X)
        
        # Main Content Frame
        content_frame = tk.Frame(self.root, bg="#121212", pady=15)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left Frame: Clock Canvas
        left_frame = tk.Frame(content_frame, bg="#121212", width=420)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        self.canvas = tk.Canvas(
            left_frame, 
            width=400, 
            height=320, 
            bg="#181818", 
            highlightthickness=1, 
            highlightbackground="#2d2d2d"
        )
        self.canvas.pack(pady=5)
        
        # Clock Status Label
        self.status_label = tk.Label(
            left_frame, 
            text="Mode: ANALOG  |  Gesture: None", 
            font=("Consolas", 12, "bold"), 
            fg="#ffffff", 
            bg="#121212"
        )
        self.status_label.pack(pady=5)
        
        # Manual switch controls
        btn_frame = tk.Frame(left_frame, bg="#121212")
        btn_frame.pack(pady=5)
        
        toggle_btn = tk.Button(
            btn_frame,
            text="Toggle Mode",
            command=self.toggle_mode,
            font=("Helvetica", 10, "bold"),
            bg="#00e5ff",
            fg="#000000",
            activebackground="#00b2cc",
            width=12
        )
        toggle_btn.pack(side=tk.LEFT, padx=10)
        
        exit_btn = tk.Button(
            btn_frame,
            text="Exit App",
            command=self.close_app,
            font=("Helvetica", 10, "bold"),
            bg="#ff5252",
            fg="#ffffff",
            activebackground="#d32f2f",
            width=12
        )
        exit_btn.pack(side=tk.LEFT, padx=10)
        
        # Right Frame: Camera Feed & Guide
        right_frame = tk.Frame(content_frame, bg="#121212", width=380)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        
        # Camera view label
        self.camera_label = tk.Label(
            right_frame, 
            width=360, 
            height=270, 
            bg="#181818",
            highlightthickness=1, 
            highlightbackground="#2d2d2d"
        )
        self.camera_label.pack(pady=5)
        
        # Instructions label
        guide_text = (
            "GESTURE CONTROL GUIDE:\n"
            "✋ Open Palm or 👎 Thumb Down  => DIGITAL Clock\n"
            "✊ Closed Fist, 👍 Thumb Up, or ✌️ Victory => ANALOG Clock\n"
            "Spacebar => Manual Toggle  |  'q' in Webcam Feed => Close Video"
        )
        guide_label = tk.Label(
            right_frame, 
            text=guide_text, 
            font=("Helvetica", 9),
            justify=tk.LEFT,
            fg="#b0bec5",
            bg="#121212",
            pady=5
        )
        guide_label.pack(pady=5)
        
        # Key bindings
        self.root.bind("<space>", lambda event: self.toggle_mode())
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
        
        # Start update loops
        self.update_clock()
        self.update_camera()
        
    def toggle_mode(self):
        self.mode = "digital" if self.mode == "analog" else "analog"
        print(f"Mode manually toggled to: {self.mode}")
        
    def update_clock(self):
        if not self.running:
            return
            
        self.canvas.delete("all")
        now = datetime.now()
        
        if self.mode == "analog":
            # Center points
            cx, cy = 200, 160
            r = 110
            
            # Clock face
            self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline="#00e5ff", width=3)
            self.canvas.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill="#00e5ff", outline="#00e5ff")
            
            # Tick marks
            for i in range(12):
                angle = i * (2 * math.pi / 12) - math.pi / 2
                is_major = (i % 3 == 0)
                r_inner = r - 15 if is_major else r - 8
                x1 = cx + r_inner * math.cos(angle)
                y1 = cy + r_inner * math.sin(angle)
                x2 = cx + r * math.cos(angle)
                y2 = cy + r * math.sin(angle)
                color = "#00e5ff" if is_major else "#888888"
                width = 3 if is_major else 1
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
                
            # Draw hour labels (12, 3, 6, 9)
            for val, ang in [(12, -math.pi/2), (3, 0), (6, math.pi/2), (9, math.pi)]:
                tx = cx + (r - 28) * math.cos(ang)
                ty = cy + (r - 28) * math.sin(ang)
                self.canvas.create_text(tx, ty, text=str(val), font=("Helvetica", 10, "bold"), fill="#ffffff")
                
            # Calculate hands
            sec = now.second + now.microsecond / 1000000.0
            minute = now.minute + sec / 60.0
            hour = (now.hour % 12) + minute / 60.0
            
            angle_sec = sec * (2 * math.pi / 60) - math.pi / 2
            angle_min = minute * (2 * math.pi / 60) - math.pi / 2
            angle_hour = hour * (2 * math.pi / 12) - math.pi / 2
            
            # Hour hand (short, thick)
            xh = cx + 55 * math.cos(angle_hour)
            yh = cy + 55 * math.sin(angle_hour)
            self.canvas.create_line(cx, cy, xh, yh, fill="#ffffff", width=5, capstyle="round")
            
            # Minute hand (medium)
            xm = cx + 80 * math.cos(angle_min)
            ym = cy + 80 * math.sin(angle_min)
            self.canvas.create_line(cx, cy, xm, ym, fill="#b0bec5", width=3, capstyle="round")
            
            # Second hand (thin, red, sweeps)
            xs = cx + 95 * math.cos(angle_sec)
            ys = cy + 95 * math.sin(angle_sec)
            self.canvas.create_line(cx, cy, xs, ys, fill="#ff5252", width=1.5)
            # Tail
            xst = cx - 15 * math.cos(angle_sec)
            yst = cy - 15 * math.sin(angle_sec)
            self.canvas.create_line(cx, cy, xst, yst, fill="#ff5252", width=1.5)
            
        else:  # Digital mode
            time_str = now.strftime("%I:%M:%S %p")
            date_str = now.strftime("%A, %B %d, %Y")
            
            self.canvas.create_text(200, 140, text=time_str, font=("Consolas", 32, "bold"), fill="#00e5ff")
            self.canvas.create_text(200, 190, text=date_str, font=("Helvetica", 14), fill="#888888")
            
        # Update Text label
        self.status_label.config(text=f"Mode: {self.mode.upper()}  |  Gesture: {self.last_gesture}")
        
        # High update frequency for analog smooth sweeping second hand
        self.root.after(40, self.update_clock)
        
    def update_camera(self):
        if not self.running:
            return
        if self.latest_frame is not None:
            try:
                # Update Image ImageTk
                self.photo = ImageTk.PhotoImage(image=self.latest_frame)
                self.camera_label.config(image=self.photo)
            except Exception as e:
                print("Error rendering camera feed:", e)
        self.root.after(30, self.update_camera)
        
    def close_app(self):
        print("Closing application...")
        self.running = False
        self.root.destroy()
        
    def run_webcam(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Camera not found or blocked. Manual control only.")
            self.camera_label.config(
                text="Webcam Not Available\n\nUse 'Toggle Mode' Button\nor Press Spacebar", 
                fg="#ff5252", 
                font=("Helvetica", 11, "bold")
            )
            return
            
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        from mediapipe.tasks import python
        from mediapipe.tasks.python import vision
        
        # Init MediaPipe gesture recognizer
        base_options = python.BaseOptions(model_asset_path=self.model_path)
        options = vision.GestureRecognizerOptions(
            base_options=base_options,
            num_hands=1,
            min_hand_detection_confidence=0.7,
            min_hand_presence_confidence=0.5
        )
        recognizer = vision.GestureRecognizer.create_from_options(options)
        
        while self.running:
            ret, frame = cap.read()
            if not ret:
                break
                
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            
            # Convert to MediaPipe Image format
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            
            gesture_result = recognizer.recognize(mp_image)
            
            # Extract gesture and update mode
            gesture_name = "None"
            if gesture_result.gestures and len(gesture_result.gestures) > 0:
                top_gesture = gesture_result.gestures[0][0]
                gesture_name = top_gesture.category_name
                score = top_gesture.score
                
                if score > 0.6:
                    self.last_gesture = f"{gesture_name} ({score:.0%})"
                    # Action control mapping
                    if gesture_name in ["Open_Palm", "Thumb_Down"]:
                        self.mode = "digital"
                    elif gesture_name in ["Closed_Fist", "Thumb_Up", "Victory"]:
                        self.mode = "analog"
                else:
                    self.last_gesture = "None"
            else:
                self.last_gesture = "None"
                
            # Draw hand skeleton overlay
            if gesture_result.hand_landmarks:
                connections = [
                    (0, 1), (1, 2), (2, 3), (3, 4),
                    (0, 5), (5, 6), (6, 7), (7, 8),
                    (0, 9), (9, 10), (10, 11), (11, 12),
                    (0, 13), (13, 14), (14, 15), (15, 16),
                    (0, 17), (17, 18), (18, 19), (19, 20),
                    (5, 9), (9, 13), (13, 17)
                ]
                for start_idx, end_idx in connections:
                    start = gesture_result.hand_landmarks[0][start_idx]
                    end = gesture_result.hand_landmarks[0][end_idx]
                    start_pos = (int(start.x * w), int(start.y * h))
                    end_pos = (int(end.x * w), int(end.y * h))
                    cv2.line(frame, start_pos, end_pos, (0, 229, 255), 2)
                    
                for i, lm in enumerate(gesture_result.hand_landmarks[0]):
                    lx, ly = int(lm.x * w), int(lm.y * h)
                    color = (255, 255, 255) if i in [4, 8, 12, 16, 20] else (0, 229, 255)
                    cv2.circle(frame, (lx, ly), 5, color, -1)
            
            # Send frame to Tkinter app resized
            frame_rgb_small = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb_small, (360, 270))
            self.latest_frame = Image.fromarray(frame_resized)
            
        cap.release()
        print("Webcam released.")


if __name__ == "__main__":
    root = tk.Tk()
    app = GestureClockApp(root, model_path)
    
    # Start webcam processing loop in background thread
    webcam_thread = threading.Thread(target=app.run_webcam, daemon=True)
    webcam_thread.start()
    
    # Start Tkinter loop
    root.mainloop()

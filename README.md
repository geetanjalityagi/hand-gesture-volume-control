# Hand Gesture Volume Controller

A real-time, computer vision-based Windows master volume controller using hand gestures. 

This application uses a standard webcam to detect hand landmarks, calculates the distance between the tip of the thumb and the index finger, and maps that distance to the system volume using the Windows Audio Session API (WASAPI) via **PyCaw**.

---

## ✨ Features

- **Real-Time Hand Tracking:** Powered by Google's **MediaPipe Hands** framework.
- **Dynamic System Control:** Directly interacts with the Windows master volume using **PyCaw** (Python Common Audio Windows).
- **Interactive Visual HUD (Heads-Up Display):**
  - **Dynamic Volume Bar:** A vertical indicator on the left side of the frame showing the current volume level.
  - **Interactive HUD Colors:**
    -  <p><strong>Color:</strong> #00FFFF (Cyan)</p>volume levels (1% – 99%).
    - 🟦 **Blue:** Muted/Minimum volume (0%).
    - 🟥 **Red:** Maximum volume (100%).
  - **Fingertip Feedback:** Displays connection lines and landmark circles matching the status color, with a magenta circle highlighting when the fingertips touch (mute).
- **Performance Monitor:** Embedded real-time FPS (Frames Per Second) counter.

---

## 🛠️ System Requirements

- **OS:** Windows (Required for PyCaw volume controls).
- **Camera:** Standard integrated or external USB webcam.
- **Python:** Python 3.8 to 3.11 recommended.

---

## 📦 Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/hand-gesture-volume-control.git
   cd hand-gesture-volume-control
   ```

2. **Set up a Virtual Environment (Optional but Recommended):**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install Dependencies:**
   Install the required libraries using pip:
   ```bash
   pip install opencv-python mediapipe pycaw numpy
   ```

---

## 🚀 How to Run

Execute the main controller script:
```bash
python VolumeController.py
```

### How to Control Volume:
- Bring your hand into the webcam's field of view.
- **Increase Volume:** Spread your **thumb** and **index finger** apart.
- **Decrease Volume:** Pinch your **thumb** and **index finger** together.
- **Exit Program:** Press the `q` key on your keyboard while focusing on the video frame.

---

## 📂 Project Structure

```
HandVolumeController/
├── HandTrackingModule.py   # Wrapper class around Mediapipe Hands for tracking & landmark estimation
├── VolumeController.py     # Main application driver (Webcam capturing, PyCaw controller, HUD drawing)
├── .gitignore              # Files to ignore in Git version control
└── README.md               # Project documentation
```

---

## 🔍 How it Works (Under the Hood)

1. **Landmark Detection:** The [HandTrackingModule.py](file:///c:/Projects/HandVolumeController/HandTrackingModule.py) processes the incoming BGR video frame, converts it to RGB, runs it through Mediapipe Hands, and returns the pixel coordinates $(x, y)$ of the hand landmarks.
2. **Distance Calculation:** We extract the positions of the thumb tip (Landmark `#4`) and index finger tip (Landmark `#8`) and calculate the Euclidean distance:
   $$\text{Distance} = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$
3. **Interpolation:**
   Using NumPy's `np.interp`, we map the physical hand distance (typically ranging from `25` to `190` pixels depending on how close you are to the camera) to two targets:
   - **System Volume:** Mapped to the system's decibel range (usually `-65.25 dB` to `0.0 dB`).
   - **HUD Visuals:** Mapped to a percentage (`0` to `100%`) and coordinate offsets for drawing the filled bar indicator.
4. **Volume Adjustment:** The mapped volume level is sent to Windows via PyCaw's `volume.SetMasterVolumeLevel()`.

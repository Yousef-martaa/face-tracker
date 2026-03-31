# filename: gui.py

import tkinter as tk
from tkinter import ttk
import cv2
import os
import sys
from PIL import Image, ImageTk


# ===== PROJECT PATH FIX =====
# Allows running GUI directly without import errors.
if __package__ is None or __package__ == "":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)


from CAM.cam import Cam


class Gui:
    """Graphical user interface.

    This class handles layout, styling, user interaction,
    and real-time rendering of the camera feed inside Tkinter.
    """

    TARGET_FPS = 30  # Controls update speed for performance balance

    def __init__(self, cam=None):
        """Initialize GUI.

        Creates main window, initializes camera manager,
        and builds the full interface.
        """
        self.root = tk.Tk()
        self.root.title("AI Camera Control")
        self.root.geometry("900x650")
        self.root.minsize(720, 520)
        self.root.configure(bg="#2c003e")

        self.camera_manager = cam if cam is not None else Cam()

        self.video_job = None
        self.video_image = None

        self._setup_style()
        self._create_widgets()

        # Ensure safe shutdown
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # =========================================================
    # STYLE
    # =========================================================

    def _setup_style(self):
        """Setup styles.

        Defines color scheme and button styles for modern UI feel.
        """
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "TButton",
            font=("Segoe UI", 12),
            padding=10
        )

        # Start button (purple)
        style.map(
            "Start.TButton",
            background=[("!active", "#6a0dad"), ("active", "#7b1fa2")],
            foreground=[("!disabled", "white")]
        )

        # Stop button (wine red)
        style.map(
            "Stop.TButton",
            background=[("!active", "#800020"), ("active", "#a8324a")],
            foreground=[("!disabled", "white")]
        )

    # =========================================================
    # UI CREATION
    # =========================================================

    def _create_widgets(self):
        """Create GUI elements.

        Builds layout including title, controls, status,
        and video display area.
        """

        # ===== TITLE =====
        title = tk.Label(
            self.root,
            text="AI Camera Controller",
            font=("Segoe UI", 22, "bold"),
            bg="#2c003e",
            fg="white"
        )
        title.pack(pady=(18, 10))

        # ===== STATUS LABEL =====
        self.status_label = tk.Label(
            self.root,
            text="Idle",
            font=("Segoe UI", 11),
            bg="#2c003e",
            fg="#bbbbbb"
        )
        self.status_label.pack(pady=(0, 10))

        # ===== CAMERA LIST =====
        self._load_cameras()

        combo_width = 24
        if self.camera_labels:
            # Width is measured in characters for ttk.Combobox.
            combo_width = max(24, min(80, max(len(label) for label in self.camera_labels)))

        self.combo = ttk.Combobox(
            self.root,
            values=self.camera_labels,
            state="readonly",
            font=("Segoe UI", 12),
            width=combo_width,
        )
        self.combo.pack(fill="x", padx=16, pady=(0, 10))

        if self.camera_indexes:
            self.combo.current(0)

        # ===== BUTTON FRAME =====
        frame = tk.Frame(self.root, bg="#2c003e")
        frame.pack(pady=(0, 12))

        self.start_btn = ttk.Button(
            frame,
            text="Start Camera",
            command=self.start_camera,
            style="Start.TButton"
        )
        self.start_btn.grid(row=0, column=0, padx=15)

        self.stop_btn = ttk.Button(
            frame,
            text="Stop Camera",
            command=self.stop_camera,
            style="Stop.TButton"
        )
        self.stop_btn.grid(row=0, column=1, padx=15)

        # Initially disable stop button
        self.stop_btn["state"] = "disabled"

        # ===== VIDEO AREA =====
        self.video_container = tk.Frame(
            self.root,
            bg="#111111"
        )
        self.video_container.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        self.video_label = tk.Label(
            self.video_container,
            text="No camera running",
            font=("Segoe UI", 12),
            bg="#111111",
            fg="#f0f0f0",
        )
        self.video_label.pack(fill="both", expand=True)

    def _load_cameras(self):
        """Load available cameras.

        Retrieves camera list from CameraManager and prepares labels.
        """
        self.cameras = self.camera_manager.detect_camera_info()
        self.camera_indexes = [cam["index"] for cam in self.cameras]
        self.camera_labels = [cam["name"] for cam in self.cameras]

    # =========================================================
    # CAMERA CONTROL
    # =========================================================

    def start_camera(self):
        """Start selected camera.

        Starts camera safely and begins rendering loop.
        """
        index = self.combo.current()

        if index == -1:
            return

        cam_index = self.camera_indexes[index]

        # Stop previous session if running
        if self.camera_manager.is_running():
            self.stop_camera()

        self.camera_manager.start(cam_index)

        # Handle failure
        if not self.camera_manager.is_running():
            self.status_label.configure(text="Failed to start camera")
            return

        # Update UI state
        self.status_label.configure(text="Camera running")
        self.start_btn["state"] = "disabled"
        self.stop_btn["state"] = "normal"

        self._update_video_frame()

    def stop_camera(self):
        """Stop camera.

        Stops camera safely and resets UI state.
        """
        if self.video_job is not None:
            self.root.after_cancel(self.video_job)
            self.video_job = None

        self.camera_manager.stop()

        self.video_label.configure(image="", text="No camera running")
        self.video_image = None

        self.status_label.configure(text="Stopped")

        self.start_btn["state"] = "normal"
        self.stop_btn["state"] = "disabled"

    # =========================================================
    # VIDEO LOOP
    # =========================================================

    def _update_video_frame(self):
        """Update video frame.

        Fetches frame from CameraManager, resizes it,
        and renders it inside the GUI in real-time.
        """
        if not self.camera_manager.is_running():
            return

        frame = self.camera_manager.read_frame()

        if frame is not None:
            # Convert BGR to RGB
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            image = Image.fromarray(rgb)

            # Get container size
            frame_h, frame_w = rgb.shape[:2]
            box_w = max(self.video_container.winfo_width(), 1)
            box_h = max(self.video_container.winfo_height(), 1)

            # Prevent bad sizes on startup
            if box_w < 50 or box_h < 50:
                box_w, box_h = 640, 360

            # Maintain aspect ratio
            scale = min(box_w / frame_w, box_h / frame_h)
            new_w = max(1, int(frame_w * scale))
            new_h = max(1, int(frame_h * scale))

            image = image.resize((new_w, new_h), Image.Resampling.LANCZOS)

            # Convert to Tk image
            self.video_image = ImageTk.PhotoImage(image=image)

            self.video_label.configure(image=self.video_image, text="")

        # Schedule next frame update
        delay = int(1000 / self.TARGET_FPS)
        self.video_job = self.root.after(delay, self._update_video_frame)

    # =========================================================
    # SHUTDOWN
    # =========================================================

    def _on_close(self):
        """Handle window close.

        Ensures camera is stopped and resources are released.
        """
        self.stop_camera()
        self.root.destroy()

    def run(self):
        """Run GUI.

        Starts the Tkinter event loop.
        """
        self.root.mainloop()

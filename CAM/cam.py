# filename: camera_manager.py

import os
import subprocess
import threading

import cv2


class Cam:
    """Handle camera operations.

    This class is responsible for detecting cameras, starting,
    stopping, and reading frames from the selected device in a
    thread-safe and stable way.
    """

    DEFAULT_MAX_CAMERAS = 5

    def __init__(self):
        """Initialize camera manager.

        Sets default state, configures OpenCV logging level,
        prepares thread-safe resources, and selects appropriate
        backend depending on operating system.
        """
        if hasattr(cv2, "utils") and hasattr(cv2.utils, "logging"):
            cv2.utils.logging.setLogLevel(cv2.utils.logging.LOG_LEVEL_ERROR)

        self.cap = None
        self.running = False
        self.current_index = None

        self.lock = threading.Lock()

        # Use DirectShow on Windows for faster and cleaner camera handling
        self.backend = cv2.CAP_DSHOW if os.name == "nt" else None

    def _open_capture(self, index):
        """Open camera capture.

        Opens the camera using the preferred backend when available.
        Falls back to default OpenCV capture on non-Windows systems.
        """
        if self.backend is None:
            return cv2.VideoCapture(index)

        return cv2.VideoCapture(index, self.backend)

    def _get_windows_camera_names(self):
        """Fetch Windows camera names.

        Uses PowerShell to retrieve user-friendly camera names.
        Returns an empty list if the operation fails or is unavailable.
        """
        if os.name != "nt":
            return []

        ps_command = (
            "Get-CimInstance Win32_PnPEntity "
            "| Where-Object { $_.PNPClass -in @('Camera','Image') -and $_.Status -eq 'OK' } "
            "| Select-Object -ExpandProperty Name"
        )

        try:
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_command],
                capture_output=True,
                text=True,
                timeout=2,
                check=False,
            )
        except Exception:
            return []

        if result.returncode != 0:
            return []

        return [line.strip() for line in result.stdout.splitlines() if line.strip()]

    def detect_camera_info(self, max_index=None):
        """Detect cameras with metadata.

        Scans available camera indexes and returns a list of dictionaries
        containing camera index and display name. Uses fast probing to
        avoid unnecessary delays.
        """
        if max_index is None:
            max_index = self.DEFAULT_MAX_CAMERAS

        cameras = []
        names = self._get_windows_camera_names()
        name_cursor = 0

        for i in range(max_index):
            cap = self._open_capture(i)

            if not cap or not cap.isOpened():
                if cap:
                    cap.release()
                continue

            # Use grab() for faster availability check instead of read()
            if cap.grab():
                if i < len(names):
                    display_name = names[i]
                elif name_cursor < len(names):
                    display_name = names[name_cursor]
                else:
                    display_name = f"Camera {i}"

                name_cursor += 1

                cameras.append({
                    "index": i,
                    "name": display_name
                })

            cap.release()

        return cameras

    def detect_cameras(self, max_index=None):
        """Detect available camera indexes.

        Returns a list of camera indexes only, extracted from
        the full camera metadata.
        """
        camera_info = self.detect_camera_info(max_index=max_index)
        return [cam["index"] for cam in camera_info]

    def start(self, index):
        """Start camera safely.

        Opens the selected camera and sets internal state.
        Uses locking to prevent race conditions in multithreaded use.
        """
        with self.lock:
            if self.running:
                return

            self.cap = self._open_capture(index)

            if not self.cap or not self.cap.isOpened():
                if self.cap:
                    self.cap.release()
                self.cap = None
                self.running = False
                return

            self.current_index = index
            self.running = True

    def stop(self):
        """Stop camera safely.

        Stops capture and releases camera resources.
        Uses locking to ensure no thread accesses the camera
        during shutdown.
        """
        with self.lock:
            self.running = False

            if self.cap is not None:
                self.cap.release()
                self.cap = None

    def read_frame(self):
        """Read frame from camera.

        Retrieves the latest frame from the camera if running.
        Uses locking to ensure thread-safe access to the capture device.
        """
        with self.lock:
            if self.cap and self.running:
                ret, frame = self.cap.read()

                if ret:
                    return frame

        return None

    def is_running(self):
        """Check camera state.

        Returns True if the camera is currently active.
        Useful for external components such as GUI or pipelines.
        """
        return self.running
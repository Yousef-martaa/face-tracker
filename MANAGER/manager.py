# filename: manager.py

from GUI.gui import Gui
from CAM.cam import Cam
from BUFFER.buffer import Buffer


class Manager:
    """System manager.

    Central orchestrator that initializes and controls all
    system components such as GUI, camera, and buffer.
    """

    def __init__(self):
        """Initialize manager.

        Creates all core components without starting execution.
        This ensures clean separation between setup and runtime.
        """
        self.cam = Cam()
        self.buffer = Buffer()

        self.gui = None

    def setup(self):
        """Setup system.

        Initializes GUI and injects shared dependencies.
        This allows GUI to operate using central system components.
        """
        self.gui = Gui(cam=self.cam)

    def run(self):
        """Run system.

        Starts the application by launching the GUI.
        """
        if self.gui is None:
            self.setup()

        self.gui.run()

    def shutdown(self):
        """Shutdown system.

        Ensures all components are stopped safely.
        """
        self.cam.stop()
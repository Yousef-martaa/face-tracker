import cv2


class FaceDetector:
    """
    Responsible ONLY for detecting if a face exists in the frame.
    """

    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

        if self.face_cascade.empty():
            raise RuntimeError("Failed to load Haar Cascade")

    def has_face(self, frame) -> bool:
        """
        Returns True if at least one face is detected.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        return len(faces) > 0
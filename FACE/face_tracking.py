import cv2

from . import mogge_config as config
from .face_identification import FaceIdentifier


class FaceTracker:
	"""Config-driven face tracking + identification utility.

	The tracker handles face detection and drawing.
	If identification is enabled, it also annotates each face with a name.
	"""

	def __init__(self):
		self.enabled = config.TRACKING_ENABLED
		self.face_cascade = None
		self.identifier = None

		if not self.enabled:
			return

		# Build the cascade path from OpenCV's bundled classifier directory.
		cascade_path = cv2.data.haarcascades + config.CASCADE_FILENAME
		self.face_cascade = cv2.CascadeClassifier(cascade_path)

		if self.face_cascade.empty():
			raise RuntimeError(f"Could not load face cascade: {cascade_path}")

		# Identification is optional and can be toggled in mogge_config.
		if config.IDENTIFICATION_ENABLED:
			self.identifier = FaceIdentifier()

	def detect_faces(self, frame):
		"""Detect faces on a BGR frame and return bounding boxes."""
		if not self.enabled or self.face_cascade is None:
			return ()

		# Haar cascades operate on grayscale images for faster detection.
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = self.face_cascade.detectMultiScale(
			gray,
			scaleFactor=config.DETECTION_SCALE_FACTOR,
			minNeighbors=config.DETECTION_MIN_NEIGHBORS,
			minSize=config.DETECTION_MIN_SIZE,
		)
		return faces

	def draw_faces(self, frame, faces):
		"""Draw face rectangles (and optional count) directly on the frame."""
		for (x, y, w, h) in faces:
			cv2.rectangle(
				frame,
				(x, y),
				(x + w, y + h),
				config.BOX_COLOR_BGR,
				config.BOX_THICKNESS,
			)

		if config.SHOW_FACE_COUNT:
			cv2.putText(
				frame,
				f"Faces: {len(faces)}",
				config.COUNT_TEXT_ORIGIN,
				cv2.FONT_HERSHEY_SIMPLEX,
				config.COUNT_TEXT_SCALE,
				config.COUNT_TEXT_COLOR_BGR,
				config.COUNT_TEXT_THICKNESS,
			)

		return frame

	def process_frame(self, frame):
		"""Detect, identify (optional), and annotate faces for one frame."""
		faces = self.detect_faces(frame)
		self.draw_faces(frame, faces)

		if self.identifier is not None and len(faces) > 0:
			identified_faces = self.identifier.identify_faces(frame, faces)
			self.identifier.draw_identifications(frame, identified_faces)

		return frame, faces

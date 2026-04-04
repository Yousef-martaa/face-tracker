"""FACE tracking configuration.

Adjust values here to tune tracking behavior without editing code.
"""

# Search-friendly list of face tracking knobs used in face_tracking.py
FACE_TRACKING_KEYWORDS = [
    "TRACKING_ENABLED",
    "CASCADE_FILENAME",
    "DETECTION_SCALE_FACTOR",
    "DETECTION_MIN_NEIGHBORS",
    "DETECTION_MIN_SIZE",
    "BOX_COLOR_BGR",
    "BOX_THICKNESS",
    "SHOW_FACE_COUNT",
    "COUNT_TEXT_ORIGIN",
    "COUNT_TEXT_SCALE",
    "COUNT_TEXT_COLOR_BGR",
    "COUNT_TEXT_THICKNESS",
]

FACE_IDENTIFICATION_KEYWORDS = [
    "IDENTIFICATION_ENABLED",
    "KNOWN_FACES_DIR",
    "UNKNOWN_LABEL",
    "IDENTIFICATION_MATCH_THRESHOLD",
    "IDENTIFICATION_SIGNATURE_SIZE",
    "IDENTIFICATION_HIST_BINS",
    "IDENTIFICATION_ALLOWED_EXTENSIONS",
    "IDENTIFICATION_TEXT_SCALE",
    "IDENTIFICATION_TEXT_THICKNESS",
    "IDENTIFICATION_TEXT_COLOR_BGR",
]

TRACKING_ENABLED = True

# Haar cascade file loaded from cv2.data.haarcascades
CASCADE_FILENAME = "haarcascade_frontalface_default.xml"

# Detection tuning
DETECTION_SCALE_FACTOR = 1.1
DETECTION_MIN_NEIGHBORS = 5
DETECTION_MIN_SIZE = (30, 30)

# Bounding box style
BOX_COLOR_BGR = (0, 255, 0)
BOX_THICKNESS = 2

# Optional face counter overlay
SHOW_FACE_COUNT = True
COUNT_TEXT_ORIGIN = (10, 30)
COUNT_TEXT_SCALE = 0.8
COUNT_TEXT_COLOR_BGR = (0, 255, 0)
COUNT_TEXT_THICKNESS = 2

# Face identification settings
IDENTIFICATION_ENABLED = True
KNOWN_FACES_DIR = "FACE/known_faces"
UNKNOWN_LABEL = "Unknown"

# Correlation score threshold in range [-1, 1].
# Higher value means stricter matching.
IDENTIFICATION_MATCH_THRESHOLD = 0.6

# Signature extraction settings
IDENTIFICATION_SIGNATURE_SIZE = (64, 64)
IDENTIFICATION_HIST_BINS = 64
IDENTIFICATION_ALLOWED_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp")

# Label drawing settings
IDENTIFICATION_TEXT_SCALE = 0.6
IDENTIFICATION_TEXT_THICKNESS = 2
IDENTIFICATION_TEXT_COLOR_BGR = (0, 255, 0)

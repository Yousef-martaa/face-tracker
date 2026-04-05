import cv2
from face_detection import FaceDetector

def run_test():
    cap = cv2.VideoCapture(0)
    detector = FaceDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        has_face = detector.has_face(frame)

        if has_face:
            print("Face detected")
        else:
            print("No face")

        cv2.imshow("Test", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_test()
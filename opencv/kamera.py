import cv2
import numpy as np

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = cap.read()
    gri = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gri = cv2.medianBlur(gri, 7)
    kenarlar = cv2.Laplacian(gri, cv2.CV_8U, ksize=5)
    ret, maske = cv2.threshold(kenarlar, 100, 255, cv2.THRESH_BINARY_INV)

    for i in range(10):
        frame = cv2.bilateralFilter(frame, 5, 5, 7)
    dst = np.zeros(gri.shape)
    dst = cv2.bitwise_and(frame, frame, mask=maske)

    cv2.imshow('Input', dst)
    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()
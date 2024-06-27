import cv2
import numpy as np

def nothing(x):
    pass

imagen = cv2.imread('src\sensor_v1.jpg')

cv2.namedWindow('PDI41')
cv2.createTrackbar('Hmin', 'PDI41', 0, 255, nothing)
cv2.createTrackbar('Hmax', 'PDI41', 255, 255, nothing)
cv2.createTrackbar('Smin', 'PDI41', 0, 255, nothing)
cv2.createTrackbar('Smax', 'PDI41', 255, 255, nothing)
cv2.createTrackbar('Vmin', 'PDI41', 0, 255, nothing)
cv2.createTrackbar('Vmax', 'PDI41', 255, 255, nothing)

while True:
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    hMin = cv2.getTrackbarPos('Hmin', 'PDI41')
    hMax = cv2.getTrackbarPos('Hmax', 'PDI41')
    sMin = cv2.getTrackbarPos('Smin', 'PDI41')
    sMax = cv2.getTrackbarPos('Smax', 'PDI41')
    vMin = cv2.getTrackbarPos('Vmin', 'PDI41')
    vMax = cv2.getTrackbarPos('Vmax', 'PDI41')

    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])

    mascara = cv2.inRange(hsv, lower, upper)

    cv2.imshow('mascara', mascara)

    # Esperar 1 milisegundo y verificar si el usuario presiona la tecla 'q' para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
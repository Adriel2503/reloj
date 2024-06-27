import cv2
import numpy as np

# Cargar la imagen
imagen = cv2.imread('src/sensor_v1.jpg')

# Convertir a escala de grises
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Aplicar un umbral para segmentar la aguja
_, mascara = cv2.threshold(gris, 55, 255, cv2.THRESH_BINARY_INV)

# Eliminar pequeñas áreas no deseadas (ruido) y mejorar la máscara
kernel = np.ones((3, 3), np.uint8)
mascara = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel)

# Mostrar la máscara
cv2.imshow('mascara', mascara)
cv2.waitKey(0)
cv2.destroyAllWindows()

import cv2
import numpy as np

# Cargar la imagen
imagen = cv2.imread('src\sensor_v1.jpg')

# Convertir a escala de grises
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Aplicar un filtro Gaussiano para reducir el ruido
gris_suave = cv2.GaussianBlur(gris, (5, 5), 0)

# Aplicar la detección de bordes de Canny
bordes = cv2.Canny(gris_suave, 50, 150)

# Crear una máscara basada en los bordes detectados
mascara = cv2.bitwise_not(bordes)

# Mostrar la máscara resultante
cv2.imshow('mascara', mascara)
cv2.waitKey(0)
cv2.destroyAllWindows()

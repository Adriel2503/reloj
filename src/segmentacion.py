import cv2
import numpy as np

# Cargar la imagen
imagen = cv2.imread('src\sensor_v1.jpg')

# Convertir a escala de grises
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Aplicar un umbral para segmentar la aguja
_, umbral = cv2.threshold(gris, 71, 255, cv2.THRESH_BINARY_INV)

# Eliminar pequeñas áreas no deseadas (ruido) y mejorar la máscara
kernel = np.ones((5, 5), np.uint8)
mascara = cv2.morphologyEx(umbral, cv2.MORPH_CLOSE, kernel)
mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)

# Encontrar contornos
contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Crear una máscara en blanco
mascara_aguja = np.zeros_like(mascara)

# Dibujar solo la aguja en la máscara en blanco
for contorno in contornos:
    area = cv2.contourArea(contorno)
    if 1973 < area < 6192:  # Ajustar este umbral según sea necesario para detectar solo la aguja
        cv2.drawContours(mascara_aguja, [contorno], -1, (255), thickness=cv2.FILLED)

# Invertir la máscara para que la aguja sea negra sobre fondo blanco
mascara_aguja_inv = cv2.bitwise_not(mascara_aguja)

# Mostrar la máscara resultante
cv2.imshow('mascara', mascara_aguja_inv)
cv2.waitKey(0)
cv2.destroyAllWindows()

import cv2
import numpy as np

def nothing(x):
    pass

# Cargar la imagen
imagen = cv2.imread('src\sensor_v1.jpg')

# Convertir a escala de grises
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Crear una ventana
cv2.namedWindow('PDI41')

# Crear barras deslizantes para ajustar los parámetros
cv2.createTrackbar('Umbral', 'PDI41', 60, 255, nothing)
cv2.createTrackbar('Area Min', 'PDI41', 1000, 10000, nothing)
cv2.createTrackbar('Area Max', 'PDI41', 5000, 20000, nothing)

while True:
    # Obtener los valores de las barras deslizantes
    umbral_val = cv2.getTrackbarPos('Umbral', 'PDI41')
    area_min = cv2.getTrackbarPos('Area Min', 'PDI41')
    area_max = cv2.getTrackbarPos('Area Max', 'PDI41')

    # Aplicar un umbral para segmentar la aguja
    _, umbral = cv2.threshold(gris, umbral_val, 255, cv2.THRESH_BINARY_INV)

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
        if area_min < area < area_max:
            cv2.drawContours(mascara_aguja, [contorno], -1, (255), thickness=cv2.FILLED)

    # Invertir la máscara para que la aguja sea negra sobre fondo blanco
    mascara_aguja_inv = cv2.bitwise_not(mascara_aguja)

    # Mostrar la máscara resultante
    cv2.imshow('mascara', mascara_aguja_inv)

    # Esperar 1 milisegundo y verificar si el usuario presiona la tecla 'q' para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

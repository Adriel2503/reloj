import cv2
import numpy as np

# Cargar la máscara segmentada
mascara_aguja = cv2.imread('src/mascara.jpg', cv2.IMREAD_GRAYSCALE)

# Mostrar la máscara segmentada para verificar su contenido
cv2.imshow('mascara_segmentada', mascara_aguja)
cv2.waitKey(0)

# Invertir la máscara para que la aguja sea blanca sobre fondo negro
mascara_aguja_inv = cv2.bitwise_not(mascara_aguja)

# Mostrar la máscara invertida para verificar
cv2.imshow('mascara_invertida', mascara_aguja_inv)
cv2.waitKey(0)

# Encontrar el contorno de la aguja
contornos, _ = cv2.findContours(mascara_aguja_inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if contornos:
    # Ajustar una línea recta a los puntos del contorno
    contorno = max(contornos, key=cv2.contourArea)
    [vx, vy, x, y] = cv2.fitLine(contorno, cv2.DIST_L2, 0, 0.01, 0.01)
    
    # Asegurarse de que los valores sean escalares
    vx, vy, x, y = vx[0], vy[0], x[0], y[0]
    
    # Calcular dos puntos en la línea ajustada
    lefty = int((-x * vy / vx) + y)
    righty = int(((mascara_aguja_inv.shape[1] - x) * vy / vx) + y)
    
    # Crear una imagen en blanco para mostrar la línea ajustada
    imagen_resultante = np.ones((mascara_aguja_inv.shape[0], mascara_aguja_inv.shape[1], 3), dtype=np.uint8) * 255

    # Calcular la intersección de la línea ajustada con la línea vertical
    height, width = imagen_resultante.shape[:2]
    interseccion_x = width // 2
    interseccion_y = int((interseccion_x - x) * vy / vx + y)
    
    # Dibujar la línea ajustada desde la intersección hacia la izquierda
    cv2.line(imagen_resultante, (interseccion_x, interseccion_y), (0, lefty), (0, 0, 0), 2)
    
    # Dibujar la línea vertical desde la intersección hacia abajo
    cv2.line(imagen_resultante, (interseccion_x, interseccion_y), (interseccion_x, height), (255, 0, 0), 2)
    
    # Calcular el ángulo entre la línea ajustada y la línea vertical usando el producto punto
    vector_aguja = np.array([vx, vy])
    vector_vertical = np.array([0, 1])
    
    dot_product = np.dot(vector_aguja, vector_vertical)
    magnitudes = np.linalg.norm(vector_aguja) * np.linalg.norm(vector_vertical)
    angle_radians = np.arccos(dot_product / magnitudes)
    angle_degrees = np.degrees(angle_radians)

    # Ajustar el ángulo para que sea de 0 a 360 grados
    if vy < 0:
        angle_degrees = 360 - angle_degrees

    print(f'Ángulo entre la aguja y la línea vertical: {angle_degrees:.2f} grados')

    # Mostrar la imagen resultante con las líneas dibujadas
    cv2.imshow('imagen_resultante', imagen_resultante)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No se encontraron contornos en la máscara segmentada.")

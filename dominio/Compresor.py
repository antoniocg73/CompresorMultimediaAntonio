from PIL import Image # Módulo `Image` de la biblioteca PIL (Pillow).
import cv2 # OpenCV (`cv2`), una biblioteca para procesar imágenes y videos.
import os
from persistencia.guardar_archivo import GuardarArchivo

class Compresor: # Clase `Compresor` para comprimir imágenes, videos, etc.

    def compress_image(self, filepath, quality): # Método para comprimir imágenes.
        try:
            img = Image.open(filepath) # Abrir la imagen en la ruta especificada.
            
            # Detectar el formato original del archivo (ejemplo: ".png", ".jpg")
            file_extension = os.path.splitext(filepath)[1].lower()

            # Generar la ruta de salida para el archivo comprimido
            output_path = filepath.replace(file_extension, f'_compressed{file_extension}')
            
            # Configurar el formato de salida en función de la extensión
            if file_extension in ['.jpg', '.jpeg']:
                output_format = 'JPEG'

                # Convertir a modo RGB si es necesario (para JPEG)
                if img.mode == 'RGBA':
                    img = img.convert('RGB')    

            elif file_extension == '.png':
                output_format = 'PNG'
            else:
                # Si el formato no es compatible, devolver un error
                return False, "Formato de imagen no compatible para compresión."
            
            # Guardar la imagen con el formato y calidad especificada
            if output_format == 'JPEG':
                img.save(output_path, output_format, quality=quality)
            elif output_format == 'PNG':
                img.save(output_path, output_format, compress_level=int((100 - quality) / 10))  # Ajustar nivel de compresión para PNG
            
            # Guardar usando la capa de persistencia
            guardar = GuardarArchivo()
            guardar.guardar_archivo(output_path)
            return True, output_path
        except Exception as e:
            return False, str(e)

    def compress_video(self, filepath, quality): # Método para comprimir videos.
        try:
            cap = cv2.VideoCapture(filepath) # Abrir el archivo de video en la ruta especificada.
            output_path = filepath.replace('.', '_compressed.') # Generar la ruta de salida para el archivo comprimido
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * quality / 100) # Calcular el ancho del video comprimido
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * quality / 100) # Calcular el alto del video comprimido
            fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Configurar el códec de video para la salida
            video_compressed = cv2.VideoWriter(output_path, fourcc, 30, (width, height)) # Crear el objeto de escritura de video

            while cap.isOpened(): # Iterar sobre los fotogramas del video
                ret, frame = cap.read() # Leer un fotograma del video
                if not ret: # Si no se pudo leer el fotograma, significa que se ha llegado al final del vídeo
                    break 
                resized_frame = cv2.resize(frame, (width, height)) # Redimensionar el fotograma
                video_compressed.write(resized_frame) # Escribir el fotograma redimensionado en el video de salida

            cap.release() # Liberar el archivo de video original
            video_compressed.release() # Liberar el archivo de video comprimido
            guardar = GuardarArchivo() 
            guardar.guardar_archivo(output_path)  # Guardamos el archivo usando la capa de persistencia
            return True, output_path
        except Exception as e: # Capturar cualquier excepción que ocurra durante la compresión del video
            print(f"Error en la compresión de la imagen: {str(e)}")
            return False, str(e)

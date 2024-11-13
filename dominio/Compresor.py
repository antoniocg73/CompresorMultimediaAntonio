from PIL import Image  # Módulo `Image` de la biblioteca PIL (Pillow).
import cv2  # OpenCV (`cv2`), una biblioteca para procesar imágenes y videos.
import os
from persistencia.guardar_archivo import GuardarArchivo  # Clase para guardar archivos.

class Compresor:
    """Clase `Compresor` para comprimir imágenes y videos con almacenamiento opcional."""

    def compress_image(self, filepath, quality, save_path=None):
        """
        Comprime una imagen y la guarda en la ubicación especificada.
        
        Parámetros:
        - filepath: ruta de la imagen original.
        - quality: nivel de calidad para la compresión (1-100).
        - save_path: ruta donde guardar la imagen comprimida. Si es None, se guarda junto a la original.

        Retorna:
        - (True, output_path): si la compresión es exitosa.
        - (False, mensaje de error): si ocurre un error.
        """
        try:
            img = Image.open(filepath)  # Abrir imagen original.
            file_extension = os.path.splitext(filepath)[1].lower()  # Obtener la extensión.

            # Generar ruta de salida si no se proporciona `save_path`.
            if save_path is None:
                save_path = filepath.replace(file_extension, f'_compressed{file_extension}')

            # Definir formato de salida según extensión.
            if file_extension in ['.jpg', '.jpeg']:
                output_format = 'JPEG'
                if img.mode == 'RGBA':
                    img = img.convert('RGB')  # Convertir a RGB si es necesario para JPEG.
            elif file_extension == '.png':
                output_format = 'PNG'
            else:
                return False, "Formato de imagen no compatible para compresión."

            # Guardar imagen con calidad especificada.
            if output_format == 'JPEG':
                img.save(save_path, output_format, quality=quality)
            elif output_format == 'PNG':
                img.save(save_path, output_format, compress_level=int((100 - quality) / 10))

            # Guardar con persistencia.
            GuardarArchivo().guardar_archivo(save_path)
            return True, save_path

        except Exception as e:
            return False, f"Error en la compresión de la imagen: {str(e)}"

    def compress_video(self, filepath, quality, save_path=None):
        """
        Comprime un video y lo guarda en la ubicación especificada.
        
        Parámetros:
        - filepath: ruta del video original.
        - quality: calidad (1-100) donde se redimensiona el video en porcentaje.
        - save_path: ruta donde guardar el video comprimido. Si es None, se guarda junto a la original.

        Retorna:
        - (True, output_path): si la compresión es exitosa.
        - (False, mensaje de error): si ocurre un error.
        """
        try:
            cap = cv2.VideoCapture(filepath)  # Abrir video original.
            if not cap.isOpened():
                return False, "No se pudo abrir el archivo de video."

            # Generar ruta de salida si no se proporciona `save_path`.
            if save_path is None:
                file_extension = os.path.splitext(filepath)[1]
                save_path = filepath.replace(file_extension, f'_compressed{file_extension}')

            # Dimensiones del video redimensionado.
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * quality / 100)
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * quality / 100)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Códec de salida.
            video_compressed = cv2.VideoWriter(save_path, fourcc, 30, (width, height))

            while cap.isOpened():  # Leer y redimensionar fotogramas.
                ret, frame = cap.read()
                if not ret:
                    break
                resized_frame = cv2.resize(frame, (width, height))
                video_compressed.write(resized_frame)

            # Liberar archivos.
            cap.release()
            video_compressed.release()

            # Guardar con persistencia.
            GuardarArchivo().guardar_archivo(save_path)
            return True, save_path

        except Exception as e:
            return False, f"Error en la compresión del video: {str(e)}"

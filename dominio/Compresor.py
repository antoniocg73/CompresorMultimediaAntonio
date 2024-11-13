from PIL import Image
import cv2
import os
from persistencia.guardar_archivo import GuardarArchivo

class Compresor:

    def compress_image(self, filepath, quality):
        try:
            img = Image.open(filepath)
            
            # Detectar el formato original del archivo (ejemplo: ".png", ".jpg")
            file_extension = os.path.splitext(filepath)[1].lower()
            
            # Configurar el formato de salida en función de la extensión
            if file_extension in ['.jpg', '.jpeg']:
                output_format = 'JPEG'
            elif file_extension == '.png':
                output_format = 'PNG'
            else:
                # Si el formato no es compatible, devolver un error
                return False, "Formato de imagen no compatible para compresión."

            # Convertir a modo RGB si es necesario (para JPEG)
            if img.mode == 'RGBA' and output_format == 'JPEG':
                img = img.convert('RGB')

            # Generar la ruta de salida para el archivo comprimido
            output_path = filepath.replace(file_extension, f'_compressed{file_extension}')
            
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

    def compress_video(self, filepath, quality):
        try:
            cap = cv2.VideoCapture(filepath)
            output_path = filepath.replace('.', '_compressed.')
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * quality / 100)
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * quality / 100)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, 30, (width, height))

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                resized_frame = cv2.resize(frame, (width, height))
                out.write(resized_frame)

            cap.release()
            out.release()
            guardar = GuardarArchivo()
            guardar.guardar_archivo(output_path)  # Guardamos el archivo usando la capa de persistencia
            return True, output_path
        except Exception as e:
            print(f"Error en la compresión de la imagen: {str(e)}")
            return False, str(e)

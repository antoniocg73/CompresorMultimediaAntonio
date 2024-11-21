from PIL import Image, ImageSequence  # Módulo `Image` de la biblioteca PIL (Pillow).
#import cv2  # OpenCV (`cv2`), una biblioteca para procesar imágenes y videos.
from moviepy.editor import VideoFileClip
from src.persistencia.guardar_archivo import SaveFile  # Clase para guardar archivos.
from pydub import AudioSegment  # Importar AudioSegment de la biblioteca pydub.
import subprocess



class Compressor:
    """Clase `Compresor` para comprimir imágenes y videos con almacenamiento opcional."""
    def __init__(self):
        self.guardarArchivo = SaveFile()
        # Usar resourcePath para encontrar ffmpeg y ffprobe
        ffmpeg_path = self.resourcePath("ffmpeg/bin/ffmpeg.exe")
        ffprobe_path = self.resourcePath("ffmpeg/bin/ffprobe.exe")

        # Configurar AudioSegment para que use estas rutas
        AudioSegment.converter = ffmpeg_path
        AudioSegment.ffprobe = ffprobe_path


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
            file_extension = self.guardarArchivo.obtain_ext(filepath)  # Obtener extensión del archivo.

            # Generar ruta de salida si no se proporciona `save_path`.
            if save_path is None:
                save_path = filepath.replace(file_extension, f'_compressed{file_extension}')

            # Definimos formato de salida según extensión y realizamos la compresión.
            if file_extension in ['.jpg', '.jpeg']:
                output_format = 'JPEG'
                if img.mode == 'RGBA':
                    img = img.convert('RGB')  # Convertir a RGB si es necesario para JPEG.
                img.save(save_path, output_format, quality=quality)

            elif file_extension == '.png':
                output_format = 'PNG'
                img.save(save_path, output_format, compress_level=int((100 - (quality+1)) / 10))

            elif file_extension == '.bmp': #Lo paso a PNG para reducir tamaño
                output_format = 'PNG'  # Usar PNG en lugar de BMP

                # Determinar el nivel de compresión para PNG
                compress_level = int((100 - quality) / 10)  # Ajustar el nivel de compresión (0 a 9)

                # Guardar la imagen en formato PNG
                img.save(save_path.replace('.bmp', '.png'), 'PNG', compress_level=compress_level)
            elif file_extension == '.tiff': # Convertir TIFF a JPEG para reducir tamaño
                output_format = 'TIFF'
                compression_mode = 'tiff_lzw'  # Método de compresión sin pérdida
                
                # Guardar el archivo TIFF con compresión LZW
                img.save(save_path, output_format, compression=compression_mode)

            elif file_extension == '.gif':
                output_format = 'GIF'
                # Lista de frames optimizados
                frames = []
                prev_frame = None

                # Usar `quality` para determinar el número de colores
                num_colors = max(32, 256 - int((100 - quality+1) * 2))  # Asegurarse de que haya al menos 32 colores

                # Iterar sobre los fotogramas de la imagen GIF
                for frame in ImageSequence.Iterator(img):
                    # Convertir el fotograma a una paleta reducida de colores según `quality`
                    frame = frame.convert("P", palette=Image.ADAPTIVE, colors=num_colors)

                    # Compara el fotograma actual con el fotograma anterior
                    if prev_frame and frame.tobytes() == prev_frame.tobytes():
                        continue  # Si es muy similar al anterior, omitirlo
                    
                    # Agregar el fotograma a la lista de frames
                    frames.append(frame)
                    prev_frame = frame  # Actualizar el fotograma anterior

                # Guardar el GIF animado comprimido con optimización
                frames[0].save(
                    save_path, 
                    save_all=True, 
                    append_images=frames[1:],  # Añadir los fotogramas restantes
                    optimize=True,  # Optimizar el tamaño del archivo
                    duration=img.info['duration'],  # Mantener la duración original de cada fotograma
                    loop=0  # Mantener la animación en bucle
                )
                
            else:
                return False, "Formato de imagen no compatible para compresión."

            # Guardar con persistencia.
            self.guardarArchivo.save_file(save_path)
            return True, save_path

        except Exception as e:
            return False, f"Error en la compresión de la imagen: {str(e)}"

    def compress_video(self, filepath, save_path=None):
        try:
            # Cargar el archivo de video
            video = VideoFileClip(filepath)

            # Obtener la extensión del archivo y seleccionar los códecs apropiados
            file_extension = self.guardarArchivo.obtain_ext(filepath)

            # Obtener las dimensiones originales
            original_width, original_height = video.size

            # Escalar solo si es necesario
            if original_height > 1080:
                new_height = 1080
                new_width = int(original_width * new_height / original_height)
                video_resized = video.resize(newsize=(new_width, new_height))
            else:
                video_resized = video  # No redimensionar si ya es más pequeño


            # Si no se especifica una ruta de salida, la generamos automáticamente
            if save_path is None:
                save_path = filepath.replace(f'.{file_extension}', f'_compressed.{file_extension}')

            # Definir códecs según el formato del archivo
            if file_extension == '.mp4': #FUNCIONA
                video_codec = 'libx264'  # Códec H.264 para MP4
                audio_codec = 'aac'      # Códec AAC para audio
            elif file_extension == '.avi': #FUNCIONA
                video_codec = 'mpeg4'    # Códec MPEG4 para AVI
                audio_codec = 'aac'      # Códec AAC para audio
            elif file_extension == '.mov': #FUNCIONA
                video_codec = 'libx264'   # Códec ProRes para MOV
                audio_codec = 'aac'      # Códec AAC para audio
            elif file_extension == '.mkv': #FUNCIONA
                video_codec = 'libx264'  # Códec H.264 para MKV
                audio_codec = 'aac'      # Códec AAC para audio
            elif file_extension == '.wmv': #FUNCIONA
                video_codec = 'wmv2'     # Códec WMV para WMV
                audio_codec = 'aac'    # Códec WMV para audio
            elif file_extension == '.mpeg': #FUNCIONA
                video_codec = 'mpeg2video' # Códec MPEG2 para MPEG
                audio_codec = 'libmp3lame'  # Códec MP3 para audio
            elif file_extension == '.webm': #FUNCIONA
                video_codec = 'libvpx' # Códec VP9 para WebM
                audio_codec = 'libvorbis' # Códec Opus para audio

            # Escribir el video comprimido con audio intacto
            video_resized.write_videofile(save_path, codec=video_codec, audio_codec=audio_codec, threads=4, preset="fast")

            # Guardar con persistencia
            self.guardarArchivo.save_file(save_path)
            return True, save_path

        except Exception as e:
            return False, f"Error al comprimir el video: {str(e)}"
    
    def compress_audio(self, filepath, quality, save_path=None):
        """
        Comprime un archivo de audio (MP3, WAV, AAC, FLAC, OGG, WMA) según la calidad especificada.
        
        Parámetros:
        - filepath: Ruta del archivo de audio a comprimir.
        - quality: Nivel de calidad de compresión (0 - 100).
        - save_path: Ruta donde guardar el archivo comprimido. Si es None, se sobrescribe el archivo original.
        
        Retorna:
        - (True, save_path) si la operación es exitosa.
        - (False, error_message) si ocurre un error.
        """
        try:
            # Cargar el archivo de audio
            audio = AudioSegment.from_file(filepath)

            # Determinar el formato de salida dependiendo de la extensión
            file_format = filepath.split('.')[-1].lower()

            # Verifica si la ruta de guardado es proporcionada, si no se asigna una predeterminada
            if save_path is None:
                save_path = filepath.replace(f'.{file_format}', f'_compressed.{file_format}')

            # Ajuste de la tasa de muestreo según la calidad
            sample_rate = 44100  # Tasa de muestreo por defecto (calidad estándar)
            
            # La calidad determina el ajuste de la tasa de muestreo, mayor nivel de compresión = mayor tasa de muestreo
            sample_rate = 8000 + (quality * 300)  # Reducir la tasa de muestreo para compresión

            # Establecer la tasa de muestreo en el archivo de audio
            audio = audio.set_frame_rate(sample_rate)

            # Exportar el archivo de audio comprimido
            if file_format in ['mp3', 'wav', 'ogg', 'mp2', 'ac3']:  # Formatos soportados por pydub
                bitrate = f"{min(max(quality, 32), 320)}k"  # Ajustar el bitrate entre 32 kbps y 320 kbps
                audio.export(save_path, format=file_format, bitrate=bitrate)
            else:
                return False, f"Formato de archivo '{file_format}' no compatible sin FFmpeg."

            return True, save_path
        except Exception as e:
            return False, f"Error al comprimir el archivo de audio: {str(e)}"
    
    def resourcePath(self, relative_path):
        return self.guardarArchivo.resourcePath(relative_path)
import os
import sys

class SaveFile:
    def save_file(self, filepath): # Se recibe la ruta del archivo a guardar
        print(f"Verificando existencia del archivo: {filepath}")  # Para ver qué ruta está siendo verificada
        if os.path.exists(filepath):
            print(f"Archivo encontrado: {filepath}") # Para ver qué ruta se encontró
            return True
        else:
            print(f"Archivo no encontrado: {filepath}") # Para ver qué ruta no se encontró
            raise FileNotFoundError("El archivo no se pudo guardar correctamente.")
    
    def obtain_ext(self, filepath):
        return os.path.splitext(filepath)[1].lower()  # Obtener la extensión.
    
    def resourcePath(self, relative_path):
        """ Devuelve la ruta absoluta del recurso, con barras hacia adelante. """
        try:
            # Carpeta temporal creada por PyInstaller
            base_path = sys._MEIPASS
        except AttributeError:
            # Directorio actual en modo desarrollo
            base_path = os.path.abspath(".")

        # Construye la ruta completa
        full_path = os.path.join(base_path, relative_path)

        # Normaliza las barras a '/'
        return full_path.replace("\\", "/")
    
    

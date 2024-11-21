from kivy.app import App
from src.presentacion.interfaz import CompressorInterface
import sys
import os


class CompresslyApp(App): # Coge como nombre Compressly
    def build(self): # Construcción la aplicación
        self.icon = self.resourcePath('imagenes/reposteria.png') # Icono de la aplicación

        return CompressorInterface()
    
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

        # Normaliza las barras a `/` (opcional para sistemas Windows)
        print(full_path.replace("\\", "/"))
        return full_path.replace("\\", "/")

if __name__ == "__main__":
    CompresslyApp().run()
 
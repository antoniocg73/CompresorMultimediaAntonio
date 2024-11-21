from kivy.app import App
from src.presentacion.interfaz import CompressorInterface
import sys
import os


class CompresslyApp(App): # Coge como nombre Compressly
    def build(self): # Construcción la aplicación
        self.icon = self.resourcePath('imagenes/reposteria.png') # Icono de la aplicación

        return CompressorInterface()
    
    def resourcePath(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
    
        return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    CompresslyApp().run()
 
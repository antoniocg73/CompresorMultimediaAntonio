from kivy.app import App
from presentacion.interfaz import CompressorInterface
#from kivy.core.window import Window


class CompresslyApp(App): # Coge como nombre Compressly
    icon = 'imagenes/reposteria.png' # Icono de la aplicación
    def build(self): # Construcción la aplicación

        return CompressorInterface()

if __name__ == "__main__":
    CompresslyApp().run()
 
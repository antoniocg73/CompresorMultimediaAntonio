from kivy.app import App
from presentacion.interfaz import CompressorInterface

class CompressorApp(App):
    
    def build(self): # Construcción la aplicación
        return CompressorInterface()

if __name__ == "__main__":
    CompressorApp().run()
 
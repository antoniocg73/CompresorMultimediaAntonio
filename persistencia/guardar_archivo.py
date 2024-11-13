import os

class GuardarArchivo:
    def guardar_archivo(self, filepath): # Se recibe la ruta del archivo a guardar
        print(f"Verificando existencia del archivo: {filepath}")  # Para ver qué ruta está siendo verificada
        if os.path.exists(filepath):
            print(f"Archivo encontrado: {filepath}") # Para ver qué ruta se encontró
            return True
        else:
            print(f"Archivo no encontrado: {filepath}") # Para ver qué ruta no se encontró
            raise FileNotFoundError("El archivo no se pudo guardar correctamente.")

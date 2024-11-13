import os

class GuardarArchivo:
    def guardar_archivo(self, filepath):
        print(f"Verificando existencia del archivo: {filepath}")  # Para ver qué ruta está siendo verificada
        if os.path.exists(filepath):
            print(f"Archivo encontrado: {filepath}")
            return True
        else:
            print(f"Archivo no encontrado: {filepath}")
            raise FileNotFoundError("El archivo no se pudo guardar correctamente.")

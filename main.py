from kivy.app import App
from presentacion.interfaz import CompressorInterface
from dominio.Compresor import Compresor
from tkinter.filedialog import asksaveasfilename

class CompressorApp(App):
    
    def build(self):
        return CompressorInterface()

    def compress_file(self, filepath, quality):
        if not filepath or filepath == "No se ha seleccionado ningún archivo":
            self.root.ids.status.text = "Seleccione un archivo para comprimir."
            return

        compressor = Compresor()  # Instanciamos la clase Compresor desde la capa de dominio
        
        # Dependiendo de la extensión, llamamos al método correspondiente
        if filepath.lower().endswith(('.png', '.jpg', '.jpeg')):
            result, temp_output_path = compressor.compress_image(filepath, quality)
        elif filepath.lower().endswith(('.mp4', '.avi')):
            result, temp_output_path = compressor.compress_video(filepath, quality)
        else:
            self.root.ids.status.text = "Formato de archivo no compatible."
            return
        
        # Si la compresión fue exitosa, abrir el diálogo de guardar como
        if result:
            save_path = asksaveasfilename(
                initialfile=temp_output_path.split('/')[-1],
                filetypes=[("JPEG Image", "*.jpg"), ("Video MP4", "*.mp4"), ("Todos los archivos", "*.*")]
            )
            
            if save_path:
                # Mover el archivo comprimido a la ubicación seleccionada
                import shutil
                shutil.move(temp_output_path, save_path)
                self.root.ids.status.text = f"Archivo comprimido guardado en: {save_path}"
            else:
                self.root.ids.status.text = "Guardado cancelado."
        else:
            self.root.ids.status.text = f"Error: {temp_output_path}"


if __name__ == "__main__":
    CompressorApp().run()

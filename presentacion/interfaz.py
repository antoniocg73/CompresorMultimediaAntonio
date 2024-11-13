from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from dominio.Compresor import Compresor
import shutil

# Ocultar la ventana principal de Tkinter, ya que solo se necesita el diálogo para seleccionar archivos y no toda la ventana.
Tk().withdraw()

Builder.load_string("""
<CompressorInterface>:
    orientation: 'vertical' # Orientación de los elementos en la interfaz
    padding: 20 # Espaciado interno de la interfaz
    spacing: 10 # Espaciado entre los elementos de la interfaz
    canvas.before:
        Color:
            rgba: 1, 0.6, 0.2, 1  # Color naranja para el fondo
        Rectangle:
            pos: self.pos
            size: self.size
                    
    Button:
        text: "Abrir navegador de archivos" 
        on_release: root.open_file_dialog() # Al presionar el botón, se ejecuta la función "open_file_dialog"
        background_normal: ''  # Elimina el fondo predeterminado de Kivy
        background_color: 0.8, 0.4, 0, 1  # Color gris para el botón
        color: 1, 1, 1, 1  # Color de texto blanco
        on_press: self.background_color = 1, 0.278, 0, 1  # Cambia a naranja al presionar
        on_release: self.background_color = 0.8, 0.4, 0, 1  # Vuelve al color original al soltar
                    
    Label:
        id: file_path # Identificador para mostrar la ruta del archivo seleccionado
        text: root.selected_file 
        size_hint_y: None 
        height: '30dp' # Altura de la etiqueta

    BoxLayout:
        orientation: 'horizontal' # Orientación de los elementos en el layout
        spacing: 10 # Espaciado entre los elementos

        Label:
            text: "Calidad de compresión (1-100):"  
        
        TextInput:
            id: quality # Identificador para el campo de entrada de la calidad
            text: '50' # Valor inicial del campo de entrada
            multiline: False # Deshabilitar la entrada de múltiples líneas
            input_filter: 'int' # Filtrar la entrada para que solo sean números enteros

    Button:
        text: "Comprimir archivo" # Texto del botón
        on_release: root.compress_file(root.selected_file, int(quality.text)) # Al presionar el botón, se ejecuta la función "compress_file"
        background_normal: ''  # Elimina el fondo predeterminado de Kivy
        background_color: 0.8, 0.4, 0, 1  # Color gris para el botón
        color: 1, 1, 1, 1  # Color de texto blanco
        on_press: self.background_color = 1, 0.278, 0, 1  # Cambia a naranja al presionar
        on_release: self.background_color = 0.8, 0.4, 0, 1  # Vuelve al color original al soltar
                    
    Label:
        id: status # Identificador para mostrar el estado de la compresión
        text: "" 
""")
#de  <50 reduce, de >=50 aumenta
class CompressorInterface(BoxLayout): # Clase para la interfaz de compresión
    selected_file = StringProperty("No se ha seleccionado ningún archivo") 

    def open_file_dialog(self): # Método para abrir el navegador de archivos
        file_path = askopenfilename(
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg"), ("Videos", "*.mp4;*.avi"), ("Todos los archivos", "*.*")]
        ) # Seleccionar archivos de imagen, video o cualquier archivo
        if file_path:
            self.selected_file = file_path  # Actualiza el archivo seleccionado
            self.ids.file_path.text = f"Archivo seleccionado: {file_path}"  # Muestra el archivo en la interfaz

    def compress_file(self, filepath, quality): # Método para comprimir el archivo seleccionado
        if not filepath or filepath == "No se ha seleccionado ningún archivo":
            self.ids.status.text = "Seleccione un archivo para comprimir."
            return

        compressor = Compresor()  # Instanciamos la clase Compresor desde la capa de dominio
        
        # Dependiendo de la extensión, llamamos al método correspondiente
        if filepath.lower().endswith(('.png', '.jpg', '.jpeg')):
            result, temp_output_path = compressor.compress_image(filepath, quality)
        elif filepath.lower().endswith(('.mp4', '.avi')):
            result, temp_output_path = compressor.compress_video(filepath, quality)
        else:
            self.ids.status.text = "Formato de archivo no compatible."
            return
        
        # Si la compresión fue exitosa, abrir el diálogo de guardar como
        if result:
            save_path = asksaveasfilename(
                initialfile=temp_output_path.split('/')[-1],
                filetypes=[("JPEG Image", "*.jpg"), ("Video MP4", "*.mp4"), ("Todos los archivos", "*.*")]
            )
            
            if save_path:
                # Mover el archivo comprimido a la ubicación seleccionada
                shutil.move(temp_output_path, save_path)
                self.ids.status.text = f"Archivo comprimido guardado en: {save_path}"
            else:
                self.ids.status.text = "Guardado cancelado."
        else:
            self.ids.status.text = f"Error: {temp_output_path}"

    

from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from dominio.Compresor import Compresor
import shutil

# Ocultar la ventana principal de Tkinter, ya que solo se necesita el diálogo para seleccionar archivos y no toda la ventana.
Tk().withdraw()

Builder.load_string("""
<CompressorInterface>:
    orientation: 'vertical'  # Orientación de los elementos en la interfaz
    padding: 20  # Espaciado interno de la interfaz
    spacing: 10  # Espaciado entre los elementos de la interfaz
    canvas.before:
        Color:
            rgba: 1, 0.6, 0.2, 1  # Color naranja para el fondo
        Rectangle:
            pos: self.pos
            size: self.size
    
    # Label para mostrar el tipo de archivo seleccionado
    Label:
        text: "Selecciona el tipo de archivo"
        size_hint_y: None
        height: '30dp'

    # BoxLayout para mostrar los botones de tipo de archivo
    BoxLayout:
        orientation: 'horizontal' 
        spacing: 10 
        id: file_buttons  # Añadir un id para poder acceder a los botones

        Button:
            text: "Imagen"
            on_release: root.set_file_type("Imagen", self)
            background_normal: ''
            background_color: (1, 0.6, 0.2, 1) if root.file_type == "Imagen" else (0.8, 0.4, 0, 1)
            color: 1, 1, 1, 1

        Button:
            text: "Video"
            on_release: root.set_file_type("Video", self)
            background_normal: ''
            background_color: (1, 0.6, 0.2, 1) if root.file_type == "Video" else (0.8, 0.4, 0, 1)
            color: 1, 1, 1, 1

        Button:
            text: "Audio"
            on_release: root.set_file_type("Audio", self)
            background_normal: ''
            background_color: (1, 0.6, 0.2, 1) if root.file_type == "Audio" else (0.8, 0.4, 0, 1)
            color: 1, 1, 1, 1

    Button:
        text: "Abrir navegador de archivos" 
        on_release: root.open_file_dialog()  # Abre el diálogo de archivos
        background_normal: ''
        background_color: 0.8, 0.4, 0, 1
        color: 1, 1, 1, 1
        on_press: self.background_color = 1, 0.278, 0, 1
        on_release: self.background_color = 0.8, 0.4, 0, 1
        disabled: root.file_type == ""  # Deshabilita el botón si no se ha seleccionado tipo de archivo

    Label:
        id: file_path  # Identificador para mostrar la ruta del archivo seleccionado
        text: root.selected_file 
        size_hint_y: None 
        height: '30dp'  # Altura de la etiqueta

    BoxLayout:
        orientation: 'horizontal'
        spacing: 10

        Label:
            text: "Calidad de compresión (1-100):"  

        TextInput:
            id: quality
            text: '50'
            multiline: False
            input_filter: 'int'

    Button:
        text: "Comprimir archivo"
        on_release: root.compress_file(root.selected_file, int(quality.text))
        background_normal: ''
        background_color: 0.8, 0.4, 0, 1
        color: 1, 1, 1, 1
        on_press: self.background_color = 1, 0.278, 0, 1
        on_release: self.background_color = 0.8, 0.4, 0, 1

    Label:
        id: status  # Identificador para mostrar el estado de la compresión
        text: "" 
""")

class CompressorInterface(BoxLayout):
    selected_file = StringProperty("No se ha seleccionado ningún archivo") 
    file_type = StringProperty("")  # Variable para el tipo de archivo seleccionado

    def set_file_type(self, file_type, button):
        """ Establece el tipo de archivo seleccionado, cambia el color del botón y deselecciona otros. """
        self.file_type = file_type
        # Desactivar la selección de otros botones
        for btn in self.ids.file_buttons.children:
            btn.background_color = (0.8, 0.4, 0, 1)  # Resetear color
        # Resaltar el botón seleccionado
        button.background_color = ((1, 0.5, 0, 1))  # Resaltar el botón seleccionado

    def open_file_dialog(self):
        """Abre el diálogo de archivos para seleccionar un archivo según el tipo seleccionado."""
        if self.file_type == "Imagen":
            file_path = askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])
        elif self.file_type == "Video":
            file_path = askopenfilename(filetypes=[("Videos", "*.mp4;*.avi")])
        elif self.file_type == "Audio":
            file_path = askopenfilename(filetypes=[("Audios", "*.mp3;*.wav")])
        else:
            file_path = None
        
        if file_path:
            self.selected_file = file_path
            self.ids.file_path.text = f"Archivo seleccionado: {file_path}"

    def compress_file(self, filepath, quality):
        #Comprimir el archivo según el tipo seleccionado y la calidad proporcionada.
        # Limpiar el texto del Label de estado al presionar el botón de compresión
        self.ids.status.text = ""
        
        if not filepath or filepath == "No se ha seleccionado ningún archivo":
            self.ids.status.text = "Seleccione un archivo para comprimir."
            return

        # Configurar el tipo de archivo y extensión de guardado en función del tipo de archivo seleccionado
        if self.file_type == "Imagen":
            extension = ".jpg"
            filetypes = [("JPEG Image", "*.jpg")]
        elif self.file_type == "Video":
            extension = ".mp4"
            filetypes = [("Video MP4", "*.mp4")]
        elif self.file_type == "Audio":
            extension = ".mp3"
            filetypes = [("Audio MP3", "*.mp3")]
        else:
            self.ids.status.text = "Formato de archivo no compatible."
            return

        # Abrir diálogo de "Guardar como" con la extensión de archivo específica según el tipo seleccionado
        save_path = asksaveasfilename(
            initialfile=f"{filepath.split('/')[-1].split('.')[0]}_compressed{extension}",
            filetypes=filetypes
        )

        if not save_path:
            self.ids.status.text = "Guardado cancelado."
            return  # Salir de la función si no se seleccionó una ruta de guardado

        # Agregar la extensión correcta al save_path si el usuario no la incluyó
        if not save_path.lower().endswith(extension):
            save_path += extension

        compressor = Compresor()  # Instanciamos la clase Compresor desde la capa de dominio
        
        # Dependiendo del tipo de archivo seleccionado, llamamos al método correspondiente con la ruta final de guardado
        if self.file_type == "Imagen" and filepath.lower().endswith(('.png', '.jpg', '.jpeg')):
            result = compressor.compress_image(filepath, quality, save_path)
        elif self.file_type == "Video" and filepath.lower().endswith(('.mp4', '.avi')):
            result = compressor.compress_video(filepath, quality, save_path)
        elif self.file_type == "Audio" and filepath.lower().endswith(('.mp3', '.wav')):
            result = compressor.compress_audio(filepath, quality, save_path)
        else:
            self.ids.status.text = "Formato de archivo no compatible."
            return

        # Mostrar el mensaje de éxito si se completó la compresión
        if result:
            self.ids.status.text = f"Archivo comprimido guardado en: {save_path}"
        else:
            self.ids.status.text = "Error en la compresión."

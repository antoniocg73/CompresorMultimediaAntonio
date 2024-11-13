from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import StringProperty
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

# Ocultar la ventana principal de Tkinter
Tk().withdraw()

Builder.load_string("""
<CompressorInterface>:
    orientation: 'vertical'
    padding: 20
    spacing: 10

    Button:
        text: "Abrir navegador de archivos"
        on_release: root.open_file_dialog()

    Label:
        id: file_path
        text: root.selected_file
        size_hint_y: None
        height: '30dp'

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
        on_release: app.compress_file(root.selected_file, int(quality.text))
    
    Label:
        id: status
        text: ""
""")
#de  <50 reduce, de >=50 aumenta
class CompressorInterface(BoxLayout):
    selected_file = StringProperty("No se ha seleccionado ningún archivo")

    def open_file_dialog(self):
        # Abre el navegador de archivos del sistema
        file_path = askopenfilename(
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg"), ("Videos", "*.mp4;*.avi"), ("Todos los archivos", "*.*")]
        )
        if file_path:
            self.selected_file = file_path  # Actualiza el archivo seleccionado
            self.ids.file_path.text = f"Archivo seleccionado: {file_path}"  # Muestra el archivo en la interfaz

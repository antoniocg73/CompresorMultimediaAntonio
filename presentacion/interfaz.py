from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from kivy.core.window import Window
from sqlalchemy import false
from dominio.Compresor import Compresor
import shutil

# Ocultar la ventana principal de Tkinter, ya que solo se necesita el diálogo para seleccionar archivos y no toda la ventana.
Tk().withdraw()

# Establecemos el tamaño específico de la ventana
Window.size = (850, 600)  
Window.icon = 'imagenes/reposteria.png'

# Establecemos el tamaño mínimo de la ventana
Window.minimum_width = 850  
Window.minimum_height = 600  



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
    
    # Logo de la aplicación (imagen)
    FloatLayout: # Diseño de superposición para las imágenes
        Image:
            source: 'imagenes/reposteria.png'  # Ruta de la imagen
            size_hint: None, None
            size: 100, 100  # Tamaño de la imagen
            pos: 0, root.height - 100  # Esquina superior izquierda

        Image:
            source: 'imagenes/reposteria.png'
            size_hint: None, None
            size: 100, 100
            pos: root.width - 100, root.height - 100  # Esquina superior derecha

        Image:
            source: 'imagenes/reposteria.png'
            size_hint: None, None
            size: 100, 100
            pos: 0, 0  # Esquina inferior izquierda

        Image:
            source: 'imagenes/reposteria.png'
            size_hint: None, None
            size: 100, 100
            pos: root.width - 100, 0  # Esquina inferior derecha 
                
    
    # Label para mostrar el tipo de archivo seleccionado
    Label:
        text: "Selecciona el tipo de archivo"
        size_hint_y: None # Desactivar el ajuste automático de altura
        height: '30dp'

    # BoxLayout para mostrar los botones de tipo de archivo
    BoxLayout:
        orientation: 'horizontal' 
        spacing: 10 
        id: file_buttons  

        Button: # Botón para seleccionar opción de imagen	
            text: "Imagen"
            on_release: root.set_file_type("Imagen", self)
            background_normal: ''
            background_color: (1, 0.6, 0.2, 1) if root.file_type == "Imagen" else (0.8, 0.4, 0, 1)
            color: 1, 1, 1, 1

        Button:  # Botón para seleccionar opción de video
            text: "Video"
            on_release: root.set_file_type("Video", self)
            background_normal: ''
            background_color: (1, 0.6, 0.2, 1) if root.file_type == "Video" else (0.8, 0.4, 0, 1)
            color: 1, 1, 1, 1

        Button: # Botón para seleccionar opción de audio
            text: "Audio"
            on_release: root.set_file_type("Audio", self)
            background_normal: ''
            background_color: (1, 0.6, 0.2, 1) if root.file_type == "Audio" else (0.8, 0.4, 0, 1)
            color: 1, 1, 1, 1

    Button: # Botón para abrir el navegador de archivos
        text: "Abrir navegador de archivos" 
        on_release: root.open_file_dialog()  # Abre el diálogo de archivos
        background_normal: ''
        background_color: 0.8, 0.4, 0, 1
        color: 1, 1, 1, 1
        on_press: self.background_color = 1, 0.278, 0, 1
        on_release: self.background_color = 0.8, 0.4, 0, 1
        disabled: root.file_type == "" or quality.focus # Deshabilita el botón si no se ha seleccionado tipo de archivo

    Label:
        id: file_path  # Identificador para mostrar la ruta del archivo seleccionado
        text: root.selected_file 
        size_hint_y: None 
        height: '30dp'  # Altura de la etiqueta
        text_size: self.size  # Ajustar el texto al tamaño de la etiqueta
        wrap: True  # Ajustar el texto si es demasiado largo
        halign: 'center'  # Alineación horizontal (puedes cambiar a 'left' o 'right' según desees)
        valign: 'middle'  # Alineación vertical
                    
    Widget: # Espacio en blanco para separar los elementos
        size_hint_y: None  # Desactivar el ajuste automático de altura
        height: '30dp'  # Ajustar el espacio entre el Label y el BoxLayout

    BoxLayout: # BoxLayout para el nivel de compresión
        orientation: 'horizontal'
        spacing: 10

        Label: 
            id: compression_label
            text: "Nivel de compresión (50 - mínima, 100 - máxima):"  
            size_hint_x: 0.6

        Button: # Botón para disminuir el nivel de compresión
            id: decrease_button
            size_hint_x: 0.2
            width: '40dp'
            background_normal: 'imagenes/LeftArrow.png'
            background_color: 0.8, 0.4, 0, 1
            color: 1, 1, 1, 1 
            on_press: root.decrease_compression()
 
        TextInput: # TextInput para ingresar el nivel de compresión
            id: quality
            text: str(root.compression_level)  # Mostrar el nivel de compresión actual
            font_size: '25sp'
            color: 1, 1, 1, 1
            size_hint_x: 0.1
            width: '40dp'
            height: '20dp'  # Ajustar la altura para que el TextInput sea más bajo
            halign: 'center'  # Centrar el texto horizontalmente
            padding: [0, (self.height - self.line_height) / 2]  # Centrar el texto verticalmente basado en la altura
            input_filter: 'int'  # Solo permitir enteros
            multiline: False  # Evitar que el texto ocupe varias líneas
            on_text_validate: root.validate_compression_level() # Validar el valor ingresado 
            on_focus: if not self.focus: root.validate_compression_level() # Validar al perder el foco
            
        Button: # Botón para aumentar el nivel de compresión
            id: increase_button
            size_hint_x: 0.2
            width: '40dp'
            background_normal: 'imagenes/RightArrow.png'
            background_color: 0.8, 0.4, 0, 1
            color: 1, 1, 1, 1
            on_press: root.increase_compression()

    Widget: # Espacio en blanco para separar los elementos
        size_hint_y: None  # Desactivar el ajuste automático de altura
        height: '30dp'  # Ajustar el espacio entre el Label y el BoxLayout

    Button: # Botón para comprimir el archivo
        text: "Comprimir archivo"
        on_release: root.compress_file(root.selected_file, int(quality.text)) # Comprimir el archivo seleccionado
        background_normal: '' 
        background_color: 0.8, 0.4, 0, 1 
        color: 1, 1, 1, 1
        on_press: self.background_color = 1, 0.278, 0, 1 # Cambiar el color al presionar
        on_release: self.background_color = 0.8, 0.4, 0, 1 # Restablecer el color al soltar 
        disabled: not root.is_valid_compression_level or quality.focus # Deshabilitar el botón si no es válido


    Label: # Label para mostrar el estado de la compresión
        id: status  # Identificador para mostrar el estado de la compresión
        text: "" 
        text_size: self.size  # Ajustar el texto al tamaño de la etiqueta
        wrap: True  # Ajustar el texto si es demasiado largo
        halign: 'center'  # Alineación horizontal (puedes cambiar a 'left' o 'right' según desees)
        valign: 'middle'  # Alineación vertical
                    
    Widget: # Espacio en blanco para separar los elementos
        size_hint_y: None  # Desactivar el ajuste automático de altura
        height: '30dp'  # Ajustar el espacio entre el Label y el BoxLayout

""")

class CompressorInterface(BoxLayout):
    
    selected_file = StringProperty("No se ha seleccionado ningún archivo") # Variable para la ruta del archivo seleccionado
    file_type = StringProperty("")  # Variable para el tipo de archivo seleccionado
    compression_level = NumericProperty(50)  # Nivel de compresión inicial en 50
    status = StringProperty("")  # Variable para el estado de la compresión
    is_valid_compression_level = BooleanProperty(false)  # Controla si el botón "Comprimir" está habilitado
    file_path_entero = StringProperty("")



    #Establece el tipo de archivo seleccionado, cambia el color del botón y deselecciona otros en las opciones de archivo.
    def set_file_type(self, file_type, button):
        self.reset_new_path_with_delay()
        #self.file_type = f"Archivo seleccionado: {file_type}"  # Formato con "Archivo seleccionado"
        self.file_type = file_type
        # Desactivar la selección de otros botones
        for btn in self.ids.file_buttons.children:
            btn.background_color = (0.8, 0.4, 0, 1)  # Resetear color
        # Resaltar el botón seleccionado
        button.background_color = ((1, 0.5, 0, 1))  # Resaltar el botón seleccionado
        if self.file_type == "Video":
            self.avoid_level_compression("No hay opción de nivel de compresión vídeos.")
        else:
            self.enter_compression_level("Ingrese el nivel de compresión deseado (50 - mínima, 100 - máxima).")

    #Abre el diálogo de archivos para seleccionar un archivo según el tipo seleccionado.
    def open_file_dialog(self):
        self.reset_new_path_with_delay()
        if self.file_type == "Imagen":
            file_path = askopenfilename(filetypes=[("Imágenes","*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff")])
        elif self.file_type == "Video":
            file_path = askopenfilename(filetypes=[("Videos", "*.mp4;*.avi;*.mov;*.mkv;*.wmv;*.webm;*.mpeg")])
        elif self.file_type == "Audio":
            file_path = askopenfilename(filetypes=[("Audios", "*.mp3;*.wav;*.ogg;*.flac;*.wma;*.aac")])
        else:
            file_path = None
        
        # Verificar si el archivo seleccionado es un archivo TIFF para evitar la opción de nivel de compresión
        if file_path.lower().endswith(".tiff"):
            self.avoid_level_compression("No hay opción de nivel de compresión para archivos TIFF.")
        elif self.file_type != "Video": # Permitir el nivel de compresión para otros formatos sin tener en cuenta videos, ya que se ajusta en otro método
            self.enter_compression_level("Ingrese el nivel de compresión deseado (50 - mínima, 100 - máxima).")

        if file_path: # Si se selecciona un archivo, actualizar la ruta del archivo
            self.selected_file = file_path
            self.file_path_entero = f"Archivo seleccionado: {file_path}" # Actualizar la etiqueta de la ruta
            self.ids.file_path.text = self.file_path_entero

    def avoid_level_compression(self, message):
            # Ocultar o deshabilitar el TextInput
            self.ids.quality.opacity = 0  # Ocultar el TextInput
            self.ids.quality.height = 0
            # Ocultar los botones
            self.ids.decrease_button.opacity = 0  # Hacer invisibles los botones
            self.ids.decrease_button.size_hint_x = None  # Quitar el espacio horizontal
            self.ids.decrease_button.width = 0  # Ajustar el ancho a 0
            self.ids.increase_button.opacity = 0
            self.ids.increase_button.size_hint_x = None
            self.ids.increase_button.width = 0


            # Mostrar un mensaje opcional
            self.ids.compression_label.text = message
            self.ids.compression_label.halign = 'center'  # Centrar el texto horizontalmente
            self.ids.compression_label.size_hint_x = None  # Permitir que el label ocupe todo el espacio
            self.ids.compression_label.width = self.width  # Ajustar el ancho del label al ancho de la ventana
    
    def enter_compression_level(self, message):
            # Restaurar el TextInput para otros archivos
            self.ids.quality.opacity = 1
            self.ids.quality.height = '20dp'
            
            # Restaurar los botones
            self.ids.decrease_button.opacity = 1  # Hacer visibles los botones
            self.ids.decrease_button.size_hint_x = 0.2  # Restaurar tamaño horizontal
            self.ids.decrease_button.width = '40dp'  # Restaurar ancho
            self.ids.increase_button.opacity = 1
            self.ids.increase_button.size_hint_x = 0.2
            self.ids.increase_button.width = '40dp'
            
            # Limpiar cualquier mensaje previo
            self.ids.compression_label.text = message
            self.ids.compression_label.halign = 'left'  # Restaurar alineación original
            self.ids.compression_label.size_hint_x = 0.6  # Reducir el ancho para ajustarse al contenido


    #Aumenta el nivel de compresión en 1 hasta un máximo de 100.
    def increase_compression(self):
        if self.compression_level < 100:
            self.compression_level += 1
            self.update_quality()

    #Disminuye el nivel de compresión en 1 hasta un mínimo de 1.
    def decrease_compression(self):
        if self.compression_level > 50:
            self.compression_level -= 1
            self.update_quality()

    #Actualizar el texto en el TextInput y cualquier etiqueta asociada
    def update_quality(self):
        self.ids.quality.text = str(self.compression_level)

    #Valida el nivel de compresión ingresado en el TextInput.
    def validate_compression_level(self):
        new_value = int(self.ids.quality.text)  # Obtener el valor del TextInput
        if 50 <= new_value <= 100:
            self.compression_level = new_value
            self.ids.quality.focus = False  # Quitar el foco del TextInput
        else:
            self.reset_compression_level()
            #self.ids.quality.text = str(self.compression_level)  # Restablecer al valor válido

    #Restablece el nivel de compresión al valor predeterminado.
    def reset_compression_level(self):
        self.compression_level = 50
        self.update_quality()
    
    #Restablece la ruta del archivo seleccionado después de un retraso de 3 segundos.
    def reset_file_path_with_delay(self):
    #Programar el restablecimiento del texto con un retraso de 3 segundos.
        Clock.schedule_once(lambda dt: self.reset_file_path(), 3)

    #Restablece la ruta del archivo seleccionado después de un retraso de 3 segundos.
    def reset_new_path_with_delay(self):
    #Programar el restablecimiento del texto con un retraso de 3 segundos.
        Clock.schedule_once(lambda dt: self.reset_new_path(), 2)

    #Restablece la ruta del archivo seleccionado.
    def reset_file_path(self):
        self.selected_file = "No se ha seleccionado ningún archivo"
        self.ids.file_path.text = self.selected_file
    
    def reset_new_path(self):
        self.status = ""
        self.ids.status.text = self.status

    def compress_file(self, filepath, quality):
        #Comprimir el archivo según el tipo seleccionado y la calidad proporcionada.
        # Limpiar el texto del Label de estado al presionar el botón de compresión
        self.status = ""
        self.ids.status.text = self.status
        
        if not filepath or filepath == "No se ha seleccionado ningún archivo":
            self.status = "Seleccione un archivo para comprimir."
            self.ids.status.text = self.status
            return

        file_extension = filepath.split('.')[-1].lower()  # Obtiene la extensión en minúsculas


        # Configurar el tipo de archivo y extensión de guardado en función del tipo de archivo seleccionado
        if self.file_type == "Imagen":
            filetypes = [("Imágenes","*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff")]
        elif self.file_type == "Video":
            filetypes = [("Videos", "*.mp4;*.avi;*.mov;*.mkv;*.wmv;*.webm;*.mpeg")]
        elif self.file_type == "Audio":
            filetypes = [("Audio MP3", "*.mp3;*.wav;*.ogg;*.flac;*.wma;*.aac")]
        else:
            self.status = "Formato de archivo no compatible."
            self.ids.status.text = self.status
            return

        # Abrir diálogo de "Guardar como" con la extensión de archivo específica según el tipo seleccionado
        save_path = asksaveasfilename(
            initialfile=f"{filepath.split('/')[-1].split('.')[0]}_compressed.{file_extension}",
            filetypes=filetypes
        )

        if not save_path:
            self.status = "Guardado cancelado."
            self.ids.status.text = self.status
            return  # Salir de la función si no se seleccionó una ruta de guardado

        # Agregar la extensión correcta al save_path si el usuario no la incluyó
        if not save_path.lower().endswith(file_extension):
            save_path += "."+ file_extension

        compressor = Compresor()  # Instanciamos la clase Compresor desde la capa de dominio
        
        # Dependiendo del tipo de archivo seleccionado, llamamos al método correspondiente con la ruta final de guardado
        # (100 - quality + 1) -> Invertimos la lógica de calidad: 1 (menor compresión) a 100 (mayor compresión)

        if self.file_type == "Imagen" and filepath.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
            result = compressor.compress_image(filepath, (100 - quality), save_path)
        elif self.file_type == "Video" and filepath.lower().endswith(('.mp4', '.avi','.mov', '.mkv', '.wmv', '.webm', '.mpeg')):
            result = compressor.compress_video(filepath, save_path)
        elif self.file_type == "Audio" and filepath.lower().endswith(('.mp3', '.wav', '.ogg', '.flac', '.wma', '.aac')):
            result = compressor.compress_audio(filepath, (100 - quality), save_path)
        else:
            self.status = "Formato de archivo no compatible."
            self.ids.status.text = self.status
            return

        # Mostrar el mensaje de éxito si se completó la compresión
        if result[0]:
            self.status = f"Archivo comprimido guardado en: {result[1]}"
            self.ids.status.text = self.status
        else:
            self.status = result[1]  # Mostrar el mensaje de error
            self.ids.status.text = self.status  # Actualizar el texto del Label de estado
        self.reset_file_path_with_delay()
        self.reset_compression_level()

    
            

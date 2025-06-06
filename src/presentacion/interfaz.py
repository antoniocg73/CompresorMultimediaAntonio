from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from kivy.core.window import Window
from sqlalchemy import false
from src.dominio.Compresor import Compressor

# Cargar el archivo kv para el diseño de la interfaz
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
            source: root.resourcePath('imagenes/reposteria.png')  # Ruta de la imagen
            size_hint: None, None # Desactivar el ajuste automático de tamaño
            size: 100, 100  # Tamaño de la imagen
            pos: 0, root.height - 100  # Esquina superior izquierda

        Image:
            source: root.resourcePath('imagenes/reposteria.png')            
            size_hint: None, None
            size: 100, 100
            pos: root.width - 100, root.height - 100  # Esquina superior derecha

        Image:
            source: root.resourcePath('imagenes/reposteria.png')            
            size_hint: None, None
            size: 100, 100
            pos: 0, 0  # Esquina inferior izquierda

        Image:
            source: root.resourcePath('imagenes/reposteria.png')            
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

        Button: # Botón para seleccionar opción de texto	
            id: text_button
            text: "Texto"
            on_release: root.set_file_type("Texto", self)
            background_normal: ''
            background_color: (1, 0.6, 0.2, 1) if root.file_type == "Texto" else (0.8, 0.4, 0, 1)
            color: 1, 1, 1, 1            

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
        disabled: root.file_type == "" or quality.focus or (root.file_type == "Texto" and root.algorithm_type == "") # Deshabilita el botón si no se ha seleccionado tipo de archivo

    Label:
        id: file_path  # Identificador para mostrar la ruta del archivo seleccionado
        text: root.selected_file 
        size_hint_y: None 
        height: '30dp'  # Altura de la etiqueta
        text_size: self.size  # Ajustar el texto al tamaño de la etiqueta
        wrap: True  # Ajustar el texto si es demasiado largo
        halign: 'center'  # Alineación horizontal 
        valign: 'middle'  # Alineación vertical
                    
    Widget: # Espacio en blanco para separar los elementos
        size_hint_y: None  # Desactivar el ajuste automático de altura
        height: '30dp'  # Ajustar el espacio entre el Label y el BoxLayout

    BoxLayout: # BoxLayout para el nivel de compresión
        id: compression_buttons
        orientation: 'horizontal'
        height: 50
        opacity: 1  # Mostrar los botones de compresión
        spacing: 10
        #size_hint_y: None  # Desactivar el ajuste automático de altura

        Label: 
            id: compression_label
            text: "Nivel de compresión (50 - mínima, 100 - máxima):"  
            size_hint_x: 0.6

        Button: # Botón para disminuir el nivel de compresión
            id: decrease_button
            size_hint_x: 0.2
            width: '40dp'  # Ancho del botón
            background_normal: root.resourcePath('imagenes/LeftArrow.png') 
            background_color: 0.8, 0.4, 0, 1
            color: 1, 1, 1, 1 
            on_press: root.decrease_compression() # Disminuir el nivel de compresión
 
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
            background_normal: root.resourcePath('imagenes/RightArrow.png') 
            background_color: 0.8, 0.4, 0, 1
            color: 1, 1, 1, 1
            on_press: root.increase_compression() # Aumentar el nivel de compresión
    
    BoxLayout: # BoxLayout para los formatos de texto
        id: algorithm_buttons
        orientation: 'horizontal'
        opacity: 0  # Ocultar los botones de algoritmo
        height: 0  # Ocultar los botones de algoritmo
        size_hint_y: None  # Desactivar el ajuste automático de altura
        spacing: 10

        Button: # Botón para seleccionar opción de deflate	
            id: deflate_button
            text: "deflate"
            on_release: root.set_algorithm_type("deflate", self)
            background_normal: ''
            background_color: (1, 0.6, 0.2, 1) if root.algorithm_type == "deflate" else (0.8, 0.4, 0, 1)
            color: 1, 1, 1, 1

        Button:  # Botón para seleccionar opción de bzip2
            id: bzip2_button
            text: "bzip2"
            on_release: root.set_algorithm_type("bzip2", self)
            background_normal: ''
            background_color: (1, 0.6, 0.2, 1) if root.algorithm_type == "bzip2" else (0.8, 0.4, 0, 1)
            color: 1, 1, 1, 1

        Button: # Botón para seleccionar opción de lzma2
            id: lzma2_button
            text: "lzma2"
            on_release: root.set_algorithm_type("lzma2", self)
            background_normal: ''
            background_color: (1, 0.6, 0.2, 1) if root.algorithm_type == "lzma2" else (0.8, 0.4, 0, 1)
            color: 1, 1, 1, 1           

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
        halign: 'center'  # Alineación horizontal 
        valign: 'middle'  # Alineación vertical
                    
    Widget: # Espacio en blanco para separar los elementos
        size_hint_y: None  # Desactivar el ajuste automático de altura
        height: '30dp'  # Ajustar el espacio entre el Label y el BoxLayout

""")

class CompressorInterface(BoxLayout): 
    
    def __init__(self, **kwargs): #
        super().__init__(**kwargs)
        self.compressor = Compressor()  # Inicializar el compresor
        # Ocultar la ventana principal de Tkinter, ya que solo se necesita el diálogo para seleccionar archivos y no toda la ventana.
        Tk().withdraw()

        # Establecemos el tamaño específico de la ventana
        Window.size = (850, 600)  
        # Establecemos el tamaño mínimo de la ventana
        Window.minimum_width = 850  
        Window.minimum_height = 600  

        #Inicio con la opción de texto marcado
        self.file_type = "Texto"
        self.set_file_type("Texto", self.ids.text_button) # Iniciar con el botón de texto seleccionado



    #En Kivy, las propiedades como StringProperty, NumericProperty, y BooleanProperty no deben asignarse dentro del __init__, sino directamente.
    selected_file = StringProperty("No se ha seleccionado ningún archivo") # Variable para la ruta del archivo seleccionado
    file_type = StringProperty("")  # Variable para el tipo de archivo seleccionado
    algorithm_type = StringProperty("")  # Variable para el tipo de algoritmo seleccionado
    compression_level = NumericProperty(50)  # Nivel de compresión inicial en 50
    status = StringProperty("")  # Variable para el estado de la compresión
    is_valid_compression_level = BooleanProperty(false)  # Controla si el botón "Comprimir" está habilitado
    file_path_entero = StringProperty("")



    #Establece el tipo de archivo seleccionado, cambia el color del botón y deselecciona otros en las opciones de archivo.
    def set_file_type(self, file_type, button):
        self.reset_new_path_with_delay()
        self.file_type = file_type
        # Desactivar la selección de otros botones
        for btn in self.ids.file_buttons.children:
            btn.background_color = (0.8, 0.4, 0, 1)  # Resetear color
        button.background_color = ((1, 0.5, 0, 1))  # Resaltar el botón seleccionado
        if self.file_type == "Video" or self.file_type == "Audio": # Si el archivo es de video o audio, no se puede seleccionar un nivel de compresión
            self.enter_compression_layout()
            self.clean_algorithm_buttons()
            self.avoid_level_compression("No hay opción de nivel de compresión de " +self.file_type + ".")
        elif self.file_type == "Texto": # Si el archivo es de texto, se puede seleccionar un algoritmo de compresión
            self.enter_algorithm_layout()
            self.avoid_level_compression("No hay opción de nivel de compresión para archivos de texto.")
        else: # Para otros tipos de archivos (imágenes), se puede seleccionar un nivel de compresión
            self.enter_compression_layout()
            self.clean_algorithm_buttons()
            self.enter_compression_level("Ingrese el nivel de compresión deseado (50 - mínima, 100 - máxima).")

    #Establece el tipo de algoritmo seleccionado, cambia el color del botón y deselecciona otros en las opciones de algoritmo.
    def set_algorithm_type(self, algorithm_type, button):
        self.reset_new_path_with_delay()
        self.algorithm_type = algorithm_type
        # Desactivar la selección de otros botones
        for btn in self.ids.algorithm_buttons.children:
            btn.background_color = (0.8, 0.4, 0, 1)  # Resetear color
        # Resaltar el botón seleccionado
        button.background_color = ((1, 0.5, 0, 1))  # Resaltar el botón seleccionado

    #Limpiar la selección del algoritmo y desmarcar los botones.
    def clean_algorithm_buttons(self):
        self.algorithm_type = ""  # Reiniciar el algoritmo seleccionado
        
        # Desmarcar los botones
        self.ids.deflate_button.background_color = (0.8, 0.4, 0, 1)
        self.ids.bzip2_button.background_color = (0.8, 0.4, 0, 1)
        self.ids.lzma2_button.background_color = (0.8, 0.4, 0, 1)

    #Abre el diálogo de archivos para seleccionar un archivo según el tipo seleccionado.
    def open_file_dialog(self): 
        self.reset_new_path_with_delay()
        if self.file_type == "Texto":
            file_path = askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        elif self.file_type == "Imagen":
            file_path = askopenfilename(filetypes=[("Imágenes","*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff")]) 
        elif self.file_type == "Video":
            file_path = askopenfilename(filetypes=[("Videos", "*.mp4;*.avi;*.mov;*.mkv;*.wmv;*.webm;*.mpeg")])
        elif self.file_type == "Audio":
            file_path = askopenfilename(filetypes=[("Audios", "*.mp3;*.ac3;*.ogg;*.mp2;*.wav")])
        else:
            file_path = None
        
        # Verificar si el archivo seleccionado es un archivo TIFF para evitar la opción de nivel de compresión
        if file_path.lower().endswith(".tiff"):
            self.avoid_level_compression("No hay opción de nivel de compresión para archivos TIFF.")
        elif self.file_type != "Video" and self.file_type != "Audio" and self.file_type != "Texto": # Permitir el nivel de compresión para otros formatos sin tener en cuenta videos, audios y texto
            self.enter_compression_level("Ingrese el nivel de compresión deseado (50 - mínima, 100 - máxima).")

        if file_path: # Si se selecciona un archivo, actualizar la ruta del archivo
            self.selected_file = file_path
            self.file_path_entero = f"Archivo seleccionado: {file_path}" # Actualizar la etiqueta de la ruta
            self.ids.file_path.text = self.file_path_entero

    #Cambiar el diseño de la interfaz para mostrar los botones de compresión y ocultar los de algoritmos.
    def enter_compression_layout(self):
        self.ids.compression_buttons.height = 50  # Mostrar compresión
        self.ids.compression_buttons.opacity = 1
        self.ids.compression_buttons.size_hint_y = 1
        self.ids.algorithm_buttons.height = 0  # Ocultar algoritmos
        self.ids.algorithm_buttons.opacity = 0
        self.ids.algorithm_buttons.size_hint_y = None

    #Cambiar el diseño de la interfaz para mostrar los botones de algoritmos y ocultar los de compresión.
    def enter_algorithm_layout(self):
        self.ids.compression_buttons.height = 0  # Ocultar compresión
        self.ids.compression_buttons.opacity = 0
        self.ids.compression_buttons.size_hint_y = 0
        self.ids.algorithm_buttons.height = 50  # Mostrar algoritmos
        self.ids.algorithm_buttons.opacity = 1
        self.ids.algorithm_buttons.size_hint_y = 1

    #Oculta el nivel de compresión y los botones de aumento y disminución.
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
    
    #Oculta el nivel de compresión y los botones de aumento y disminución.
    def enter_compression_level(self, message):
            # Restaurar el TextInput para otros archivos
            self.ids.quality.opacity = 1
            self.ids.quality.height = '20dp'
            
            # Restaurar los botones
            self.ids.decrease_button.opacity = 1  # Hacer visibles los botones
            self.ids.decrease_button.size_hint_x = 0.2  # Restaurar tamaño horizontal
            self.ids.increase_button.opacity = 1
            self.ids.increase_button.size_hint_x = 0.2
            
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
        if self.ids.quality.text != "":
            new_value = int(self.ids.quality.text)  # Obtener el valor del TextInput
            if 50 <= new_value <= 100:
                self.compression_level = new_value
                self.ids.quality.focus = False  # Quitar el foco del TextInput
            else:
                self.reset_compression_level()
        else:
            self.reset_compression_level()

    #Restablece el nivel de compresión al valor predeterminado.
    def reset_compression_level(self):
        self.compression_level = 50
        self.update_quality()
    
    #Restablece la ruta del archivo seleccionado después de un retraso de 3 segundos.
    def reset_file_path_with_delay(self):
    #Programar el restablecimiento del texto con un retraso de 3 segundos.
        Clock.schedule_once(lambda dt: self.reset_file_path(), 3)

    #Restablece la ruta del archivo seleccionado después de un retraso de 2 segundos.
    def reset_new_path_with_delay(self):
    #Programar el restablecimiento del texto con un retraso de 2 segundos.
        Clock.schedule_once(lambda dt: self.reset_new_path(), 2)

    #Restablece la ruta del archivo seleccionado.
    def reset_file_path(self):
        self.selected_file = "No se ha seleccionado ningún archivo"
        self.ids.file_path.text = self.selected_file
    
    #Restablece el texto del Label de estado.
    def reset_new_path(self):
        self.status = ""
        self.ids.status.text = self.status

    #Comprime el archivo seleccionado según el tipo y la calidad especificados.
    def compress_file(self, filepath, quality):
        self.status = ""
        self.ids.status.text = self.status
        
        # Verificar si se seleccionó un archivo
        if not filepath or filepath == "No se ha seleccionado ningún archivo":
            self.status = "Seleccione un archivo para comprimir."
            self.ids.status.text = self.status
            return

        # Configurar el tipo de archivo y extensión de guardado en función del tipo de archivo seleccionado
        if self.file_type == "Texto":
            filetypes = [("Archivos de texto", "*.zip;*.bz2;*.xz")]
        elif self.file_type == "Imagen":
            filetypes = [("Imágenes","*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff")]
        elif self.file_type == "Video":
            filetypes = [("Videos", "*.mp4;*.avi;*.mov;*.mkv;*.wmv;*.webm;*.mpeg")]
        elif self.file_type == "Audio":
            filetypes = [("Audio MP3", "*.mp3;*.ac3;*.ogg;*.mp2;*.wav")]
        else:
            self.status = "Formato de archivo no compatible."
            self.ids.status.text = self.status
            return

        # Obtener la extensión del archivo que se va a comprimir de texto
        if self.file_type == "Texto":
            self.status = f"El formato de texto se va a comprimir utilizando el algoritmo {self.algorithm_type}."
            self.ids.status.text = self.status
            
            # Establecer la extensión en función del algoritmo de compresión
            if self.algorithm_type.lower() == "deflate":
                file_extension = "zip"
            elif self.algorithm_type.lower() == "bzip2":
                file_extension = "bz2"
            elif self.algorithm_type.lower() == "lzma2":
                file_extension = "xz"
            else:
                file_extension = "zip"  # Por defecto usa zip si no se selecciona un algoritmo
        else:
            # Para otros tipos de archivos, se obtiene la extensión de la ruta de archivo original
            file_extension = filepath.split('.')[-1].lower()  # Obtiene la extensión en minúsculas
       
        #Comprobar si es .bmp
        if file_extension == "bmp":
            self.status = "El formato BMP se va a comprimir como png."
            self.ids.status.text = self.status
            file_extension = "png"

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
        
        # Dependiendo del tipo de archivo seleccionado, llamamos al método correspondiente con la ruta final de guardado
        # (100 - quality + 1) -> Invertimos la lógica de calidad: 1 (menor compresión) a 100 (mayor compresión)
        if self.file_type == "Texto" and filepath.lower().endswith(('.txt')):
            result = self.compressor.compress_text(filepath, save_path, self.algorithm_type)
        elif self.file_type == "Imagen" and filepath.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
            result = self.compressor.compress_image(filepath, (100 - quality), save_path)
        elif self.file_type == "Video" and filepath.lower().endswith(('.mp4', '.avi','.mov', '.mkv', '.wmv', '.webm', '.mpeg')):
            result = self.compressor.compress_video(filepath, save_path)
        elif self.file_type == "Audio" and filepath.lower().endswith(('.mp3', '.ac3', '.ogg', '.mp2', '.wav')):
            result = self.compressor.compress_audio(filepath, 0, save_path) #Le paso 0 porque en muchos niveles la compresión es igual, así que directamente lo reduzco al máximo
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
        
    # Devuelve la ruta absoluta del recurso, con barras hacia adelante.
    def resourcePath(self, relative_path):
        if not hasattr(self, 'compressor'):
            self.compressor = Compressor()  # Asegurarse de que el compresor esté inicializado
        return self.compressor.resourcePath(relative_path)

    
            

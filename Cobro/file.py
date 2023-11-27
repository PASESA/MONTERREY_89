
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from operacion import Operacion
import controller_email as tool_email 
from datetime import datetime
from os import path
from tkinter import messagebox as mb


# Nombre del estacionamiento
nombre_estacionamiento = 'Monterrey 89'.replace(" ", "_")

# Datos de acceso a la cuenta de correo
username = 'monterrey89@pasesa.com.mx'
password = '#Monterrey89'

# Correos para enviar la informacion
EMAIL_send_corte = "sistemas@pasesa.com.mx"#"ingresos@pasesa.com.mx"

class View_image:
    """Clase de la vista del login."""
    def __init__(self):
        self.DB=Operacion()
        self.opciones_corte = self.DB.obtener_lista_de('Cortes', 'Folio', 'D')

        # Crea la ventana principal
        self.window = tk.Toplevel()

        # Establece el tamaño de la ventana y su título
        self.window.title(f'Cargar imagen')

        # Establece que la ventana no sea redimensionable
        self.window.resizable(False, False)

        # Crea las variables
        self.image = tk.StringVar()
        self.variable_numero_corte = tk.IntVar()
        self.file_to_send = None

        # Llama al método "interface()" para construir la interfaz gráfica
        self.interface()

        # Inicia el loop principal de la ventana
        self.window.mainloop()

    def interface(self):
        """Define la interfaz gráfica de usuario."""
        # Crea un frame principal para la ventana
        self.seccion_principal = ttk.LabelFrame(self.window)
        self.seccion_principal.grid(row=0, column=0)

        # Crea la etiqueta para el campo de entrada de texto del nombre de usuario
        etiqueta_user = ttk.Label(self.seccion_principal, text='Seleccionar imagen: ')
        etiqueta_user.grid(row=0, column=0, padx=5, pady=5)

        self.boton_entrar = ttk.Button(self.seccion_principal, text='Cargar imagen', command=self.load_image)
        self.boton_entrar.grid(row=0, column=1, padx=5, pady=5)


        etiqueta_user = ttk.Label(self.seccion_principal, text='Seleccionar el corte: ')
        etiqueta_user.grid(row=1, column=0, padx=5, pady=5)

        self.lista_desplegable_corte = ttk.Combobox(self.seccion_principal,  values=self.opciones_corte, textvariable=self.variable_numero_corte, state='readonly', height=10, width=10)
        self.lista_desplegable_corte.current(0)
        self.lista_desplegable_corte.grid(row=1, column=1, padx=5, pady=5)

        self.seccion_imagen = ttk.Frame(self.window)
        self.seccion_imagen.grid(row=1, column=0)

        # Crea la etiqueta para el campo de entrada de texto del nombre de usuario
        self.imagen = ttk.Label(self.seccion_imagen)
        self.imagen.grid(row=0, column=0, padx=5, pady=5)

        # Crea el botón para ingresar los datos del usuario y llama al método get_data del controlador para procesar los datos
        self.boton_enviar = ttk.Button(self.seccion_imagen, text='Enviar', command=self.send_image)
        self.boton_enviar.grid(row=1, column=0, padx=5, pady=5)

    def load_image(self):
        self.file_to_send = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;"), ("Todos los archivos", "*.*")])

        # Cargar la imagen con PIL
        image = Image.open(self.file_to_send)
        image = image.resize((image.width // 3, image.height // 3), Image.ANTIALIAS)  # Cambiar tamaño de la imagen
        image = ImageTk.PhotoImage(image)

        # Configurar la imagen en el Label
        self.imagen.configure(image=image)
        self.imagen.image = image

        print(self.file_to_send)

    def send_image(self):
        # Inicializar herramientas de correo electronico y envío
        email_corte = tool_email.SendEmail(
            username=username, 
            password=password, 
            estacionamiento=nombre_estacionamiento)

        zip_file = tool_email.tools.compress_to_zip(source=self.file_to_send, output_filename=f"../Tikets/comprobante_pago_corte_{self.variable_numero_corte.get()}.zip")

        # Crear el asunto y mensaje del correo
        hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        subject = f"[{nombre_estacionamiento}]-[{hora}] Envio de {path.basename(zip_file).replace('_', ' ')[:-4]}"
        message = f"Corte del estacionamiento: {nombre_estacionamiento}."

        # Enviar el correo y manejar el resultado
        if email_corte.send_mail(to_email=EMAIL_send_corte, subject=subject, message=message, zip_file=zip_file):
            mb.showinfo("Informacion", f"Comprobante de pago del corte [{self.variable_numero_corte.get()}] enviado exitosamente")
        else:
            mb.showinfo("Informacion", f"Error: No se pudo enviar comprobante de pago del corte")

View_image()



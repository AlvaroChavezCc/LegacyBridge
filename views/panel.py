import customtkinter
import subprocess
import sys
from customtkinter import (
     CTkLabel,
     CTkButton,
     CTkFrame,
     CTkScrollableFrame,
     CTkTextbox
)


class ModuloSistema:
     def __init__(self, name, command, button, type="node"):
          self.name = name
          self.command = command
          self.button = button
          self.type = type  # "node" o "python"
          self.subprocess = None
          self.active = None

     def toggle(self):
          if not self.active:
               self.subprocess = subprocess.Popen(self.command)
               self.button.configure(fg_color=COLOR_VERDE)
               self.active = True
          else:
               self.subprocess = terminar_subproceso(self.subprocess)
               self.button.configure(fg_color=COLOR_ROJO)
               self.active = False

     def detener(self):
          self.subprocess = terminar_subproceso(self.subprocess)
          self.button.configure(fg_color=COLOR_ROJO)
          self.active = False


# CREAR BOTONES (PARA NO REPETIR CÓDIGO)
def create_button(app, desc):
     return CTkButton(
          app,
          text=desc,
          font=LABEL_FONT,
          width=150,
          height=100,
          fg_color=COLOR_ROJO,
          bg_color="transparent",
          hover_color="gray"
     )


# INICIAR FRAMEWORK
subproc_js =  subprocess.Popen(['node', './legacybridge-framework/app.js'])

# TERMINAR SUBPROCESO
def terminar_subproceso(subproc):
     if subproc is not None and hasattr(subproc, 'poll') and subproc.poll() is None:
          subproc.terminate()
          try:
               subproc.wait(timeout=5)
          except subprocess.TimeoutExpired:
               subproc.kill()
          return None
     return subproc


# CERRAR APLICACIÓN Y TERMINAR SUBPROCESOS (INCLUIDO EL FRAMEWORK)
def on_closing():
     ventas.detener()
     inventario.detener()
     contabilidad.detener()

     global subproc_js
     subproc_js = terminar_subproceso(subproc_js)
     
     app.destroy()
     sys.exit()


# CONFIGURACIÓN DE ESTILOS
customtkinter.set_appearance_mode("light")
LABEL_FONT = ("Verdana", 18)
CHECKER_FONT = ("Verdana", 16)
TITLE_FONT = ("Verdana", 25)
COLOR_ROJO = "#e01a1a"
COLOR_BLANCO = "#ffffff"
COLOR_NEGRO = "#000000"
COLOR_VERDE = "#0a7f1d"
COLOR_AMBAR = "#eedf2c"


# INICIAR APLICACIÓN
app = customtkinter.CTk()
app.protocol("WM_DELETE_WINDOW", on_closing)
app.geometry("800x600")
app.title("Panel de Control LegacyBridge")


# VENTANA PRINCIPAL
frame_data = CTkFrame(app, width=800, height=600, corner_radius=0)
frame_data.pack(fill="both", expand=True)
frame_data.columnconfigure((0,1,2), weight=1)
frame_data.rowconfigure((0,1,2), weight=1)


# TÍTULO
label_titulo = CTkLabel(
     frame_data,
     text="Panel de Control",
     font=TITLE_FONT,
     text_color=COLOR_NEGRO
)
label_titulo.grid(row=0, column=0, columnspan=3)


# BOTONES DE VENTAS, INVENTARIO Y CONTABILIDAD
button_ventas = create_button(frame_data, "Ventas")
button_ventas.grid(row=1, column=0, padx=0)

button_inventario = create_button(frame_data, "Inventario")
button_inventario.grid(row=1, column=1)

button_contabilidad = create_button(frame_data, "Contabilidad")
button_contabilidad.grid(row=1, column=2)


# MÓDULOS
ventas = ModuloSistema("Ventas", ['node', './systems/ventas/index.js'], button_ventas)
inventario = ModuloSistema("Inventario", ['python', './wrappers/wrapper_inventario.py'], button_inventario)
contabilidad = ModuloSistema("Contabilidad", ['python', './systems/inventario/legacy_inventory.py'], button_contabilidad)

# ASIGNAR COMANDOS A LOS BOTONES
button_ventas.configure(command=ventas.toggle)
button_inventario.configure(command=inventario.toggle)
button_contabilidad.configure(command=contabilidad.toggle)


# FRAME CON SCROLL
frame_scroll = CTkScrollableFrame(
     frame_data,
     width=200,
     height=100,
     fg_color=COLOR_AMBAR,
     bg_color="transparent",
     corner_radius=10
)
frame_scroll.grid(row=2, column=0, columnspan=3, pady=20, padx=20, sticky="nsew")


# TEXTBOX PARA MOSTRAR MENSAJES DEL FRAMEWORK Y SUBPROCESOS
textbox_checker = CTkTextbox(
     frame_scroll,
     width=700,
     height=200,
     font=CHECKER_FONT,
     wrap="word"
)
textbox_checker.pack(padx=10, pady=10, anchor="w")

# CONTINUAR EJECUTANDO LA APLICACIÓN
app.mainloop()

import customtkinter
import subprocess
import sys
import threading
from customtkinter import (
     CTkLabel,
     CTkButton,
     CTkFrame,
     CTkTextbox
)


def steam_to_textbox(stream, textbox, prefix=""):
     while True:
          line = stream.readline()
          if not line:
               break
          textbox.after(0, lambda t=prefix + line: append_textbox(textbox, t))
     stream.close()


def append_textbox(textbox, text):
     textbox.configure(state="normal")
     textbox.insert("end", text)
     textbox.see("end")
     textbox.configure(state="disabled")


class ModuloSistema:
     def __init__(self, name, command, button, textbox, type="node"):
          self.name = name
          self.command = command
          self.button = button
          self.type = type  # "node" o "python"
          self.subprocess = None
          self.active = None
          self.textbox = textbox
          self.stdout_thread = None
          self.stderr_thread = None

     def toggle(self):
          if not self.active:
               self.subprocess = subprocess.Popen(
                    self.command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    bufsize=1,
                    text=True
               )

               self.button.configure(fg_color=COLOR_VERDE)
               self.active = True

               # Hilos para leer stdout y stderr
               self.stdout_thread = threading.Thread(
                    target=steam_to_textbox,
                    args=(self.subprocess.stdout, self.textbox, f"{self.name} (stdout): "),
                    daemon=True
               )

               self.stderr_thread = threading.Thread(
                    target=steam_to_textbox,
                    args=(self.subprocess.stderr, self.textbox, f"{self.name} (stderr): "),
                    daemon=True
               )

               self.stdout_thread.start()
               self.stderr_thread.start()

          else:
               self.subprocess = terminar_subproceso(self.subprocess)
               self.button.configure(fg_color=COLOR_ROJO)
               self.active = False

     def detener(self):
          self.subprocess = terminar_subproceso(self.subprocess)
          self.button.configure(fg_color=COLOR_ROJO)
          self.active = False

          if self.stdout_thread and self.stdout_thread.is_alive():
               self.stdout_thread.join(timeout=1)
          if self.stderr_thread and self.stderr_thread.is_alive():
               self.stderr_thread.join(timeout=1)
          self.stdout_thread = None
          self.stderr_thread = None


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
     text="PANEL DE CONTROL - GRUPO 4 (ARQUITECTURA DE SOFTWARE)",
     wraplength=500,
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


# FRAME CON SCROLL
frame_data = CTkFrame(
     frame_data,
     width=200,
     height=100,
     fg_color=COLOR_AMBAR,
     bg_color="transparent",
     corner_radius=10
)
frame_data.grid(row=2, column=0, columnspan=3, pady=20, padx=20, sticky="nsew")


# TEXTBOX PARA MOSTRAR MENSAJES DEL FRAMEWORK Y SUBPROCESOS
textbox_checker = CTkTextbox(
     frame_data,
     width=700,
     height=200,
     font=CHECKER_FONT,
     wrap="word"
)
textbox_checker.pack(padx=10, pady=10, anchor="w", fill="both", expand=True)
textbox_checker.configure(state="disabled")

# INICIAR FRAMEWORK
subproc_js =  subprocess.Popen(
     ['node', './legacybridge-framework/app.js'],
     stdout=subprocess.PIPE,
     stderr=subprocess.PIPE,
     bufsize=1,
     text=True
)

# Hilos para leer stdout y stderr del framework
threading.Thread(
     target=steam_to_textbox,
     args=(subproc_js.stdout, textbox_checker, "Fw (stdout): "),
     daemon=True
).start()

threading.Thread(
     target=steam_to_textbox,
     args=(subproc_js.stderr, textbox_checker, "Fw (stderr): "),
     daemon=True
).start()


# MÓDULOS
ventas = ModuloSistema(
     "Ventas",
     ['node', './systems/ventas/index.js'],
     button_ventas,
     textbox_checker
)

inventario = ModuloSistema(
     "Inventario",
     ['python', './wrappers/wrapper_inventario.py'],
     button_inventario,
     textbox_checker
)

contabilidad = ModuloSistema(
     "Contabilidad",
     ['python', './systems/inventario/legacy_inventory.py'],
     button_contabilidad,
     textbox_checker
)


# ASIGNAR COMANDOS A LOS BOTONES
button_ventas.configure(command=ventas.toggle)
button_inventario.configure(command=inventario.toggle)
button_contabilidad.configure(command=contabilidad.toggle)


# CONTINUAR EJECUTANDO LA APLICACIÓN
app.mainloop()

import customtkinter
import subprocess
import sys
from customtkinter import CTkLabel, CTkButton, CTkFrame, CTkScrollableFrame

# FUNCIÓN BOTONES
def create_button(app, desc, command=None):
     return CTkButton(
          app,
          text=desc,
          font=LABEL_FONT,
          width=150,
          height=100,
          fg_color=COLOR_ROJO,
          bg_color="transparent",
          hover_color="gray",
          command=command
     )

# Estados de activación
active_ventas = False
active_inventario = False
active_contabilidad = False

# Subprocesos
subproc_ventas = False
subproc_inventario = None
subproc_contabilidad = None

# Inicia el subproceso del framework al ejecutar la aplicación
subproc_js = subprocess.Popen(['node', './legacybridge-framework/app.js'])


# FUNCIONES
def terminar_subproceso(subproc):
     if subproc is not None and hasattr(subproc, 'poll') and subproc.poll() is None:
          subproc.terminate()
          try:
               subproc.wait(timeout=5)
          except subprocess.TimeoutExpired:
               subproc.kill()
          return None
     return subproc


# Activar subproceso de ventas
def toggle_ventas():
     global active_ventas, subproc_ventas
     if not active_ventas:
          subproc_ventas = terminar_subproceso(subproc_ventas)
          subproc_ventas = subprocess.Popen(['node', './systems/ventas/index.js'])
          button_ventas.configure(fg_color=COLOR_VERDE)
          active_ventas = True
     else:
          subproc_ventas = terminar_subproceso(subproc_ventas)
          button_ventas.configure(fg_color=COLOR_ROJO)
          active_ventas = False


def toggle_inventario():
     global active_inventario, subproc_inventario
     if not active_inventario:
          subproc_inventario = terminar_subproceso(subproc_inventario)
          subproc_inventario = subprocess.Popen(['python', './wrappers/wrapper_inventario.py'])
          button_inventario.configure(fg_color=COLOR_VERDE)
          active_inventario = True
     else:
          subproc_inventario = terminar_subproceso(subproc_inventario)
          button_inventario.configure(fg_color=COLOR_ROJO)
          active_inventario = False


def toggle_contabilidad():
     """global active_contabilidad, subproc_contabilidad
     if not active_contabilidad:
          subproc_contabilidad = terminar_subproceso(subproc_contabilidad)
          subproc_contabilidad = subprocess.Popen(['python', './systems/inventario/legacy_inventory.py'])
          button_contabilidad.configure(fg_color=COLOR_VERDE)
          active_contabilidad = True
     else:
          subproc_contabilidad = terminar_subproceso(subproc_contabilidad)
          button_contabilidad.configure(fg_color=COLOR_ROJO)
          active_contabilidad = False"""
     
     print("No activa algo importante todavía")

# Cierra el subproceso del framework y los demás al cerrar la aplicación
def on_closing():
     global subproc_js, subproc_ventas, subproc_inventario, subproc_contabilidad
     
     # Terminar los subprocesos (incluido el framework)
     subproc_js = terminar_subproceso(subproc_js)
     subproc_ventas = terminar_subproceso(subproc_ventas)
     subproc_inventario = terminar_subproceso(subproc_inventario)
     subproc_contabilidad = terminar_subproceso(subproc_contabilidad)
     
     app.destroy()
     sys.exit()


customtkinter.set_appearance_mode("light")
LABEL_FONT = ("Verdana", 18)
CHECKER_FONT = ("Verdana", 16)
TITLE_FONT = ("Verdana", 25)
COLOR_ROJO = "#e01a1a"
COLOR_BLANCO = "#ffffff"
COLOR_NEGRO = "#000000"
COLOR_VERDE = "#0a7f1d"
COLOR_AMBAR = "#eedf2c"


app = customtkinter.CTk()
app.protocol("WM_DELETE_WINDOW", on_closing)
app.geometry("800x600")
app.title("Panel de Control LegacyBridge")


frame_data = CTkFrame(app, width=800, height=600, corner_radius=0)
frame_data.pack(fill="both", expand=True)
frame_data.columnconfigure((0,1,2), weight=1)
frame_data.rowconfigure((0,1,2), weight=1)


label_titulo = CTkLabel(
     frame_data,
     text="Panel de Control",
     font=TITLE_FONT,
     text_color=COLOR_NEGRO
)
label_titulo.grid(row=0, column=0, columnspan=3)


# BOTONES
button_ventas = create_button(frame_data, "Ventas", toggle_ventas)
button_ventas.grid(row=1, column=0, padx=0)

button_inventario = create_button(frame_data, "Inventario", toggle_inventario)
button_inventario.grid(row=1, column=1)

button_contabilidad = create_button(frame_data, "Contabilidad", toggle_contabilidad)
button_contabilidad.grid(row=1, column=2)


# FRAME DE HEALTHCHECKER
"""frame_checker = CTkFrame(
     frame_data,
     width=200,
     height=100,
     fg_color=COLOR_AMBAR,
     bg_color="transparent",
     corner_radius=10
)
frame_checker.grid(row=2, column=0, columnspan=3, pady=20, padx=20, sticky="nsew")"""

frame_scroll = CTkScrollableFrame(
     frame_data,
     width=200,
     height=100,
     fg_color=COLOR_AMBAR,
     bg_color="transparent",
     corner_radius=10
)
frame_scroll.grid(row=2, column=0, columnspan=3, pady=20, padx=20, sticky="nsew")

label_checker = CTkLabel(frame_scroll, text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec vitae dictum lectus. Aliquam bibendum elit sed sem bibendum placerat.", font=CHECKER_FONT, wraplength=700, justify="left")
label_checker.pack(padx=10, pady=10, anchor="w")

app.mainloop()

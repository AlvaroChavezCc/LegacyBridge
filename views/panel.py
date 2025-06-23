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
          fg_color=COLOR_RED,
          bg_color="transparent",
          hover_color="gray",
          command=command
     )

# Iniciar procesos como None
subproc_vent_py = None
subproc_inven_py = None
subproc_cont_py = None

# FUNCIONES

# Inicia el subproceso del framework al ejecutar la aplicación
subproc_js = subprocess.Popen(['node', './legacybridge-framework/app.js'])

# Activar subproceso de ventas
def active_ventas():
     # Servicio de ventas
     subproc_vent_py = subprocess.Popen(['node', './systems/ventas/index.js'])


# Servicios de inventario
subproc_inven_py = subprocess.Popen(['python', './systems/inventario/legacy_inventory.py'])

# Servicio de contabilidad
subproc_cont_py = subprocess.Popen(['python', './wrappers/wrapper_inventario.py'])


# Cierra el subproceso del framework y los demás al cerrar la aplicación
def on_closing():
     # Termina el subproceso de framework
     if subproc_js.poll() is None:
          subproc_js.terminate()
          try:
               subproc_js.wait(timeout=5)
          except subprocess.TimeoutExpired:
               subproc_js.kill()
     
     # Termina el subproceso de ventas
     if subproc_vent_py.poll() is None:
          subproc_vent_py.terminate()
          try:
               subproc_vent_py.wait(timeout=5)
          except subprocess.TimeoutExpired:
               subproc_vent_py.kill()
     
     # Termina el subproceso de inventario
     if subproc_inven_py.poll() is None:
          subproc_inven_py.terminate()
          try:
               subproc_inven_py.wait(timeout=5)
          except subprocess.TimeoutExpired:
               subproc_inven_py.kill()

     # Termina el subproceso de contabilidad
     if subproc_cont_py.poll() is None:
          subproc_cont_py.terminate()
          try:
               subproc_cont_py.wait(timeout=5)
          except subprocess.TimeoutExpired:
               subproc_cont_py.kill()
     
     app.destroy()
     sys.exit()

customtkinter.set_appearance_mode("light")
LABEL_FONT = ("Verdana", 18)
CHECKER_FONT = ("Verdana", 16)
TITLE_FONT = ("Verdana", 25)
COLOR_RED = "#e01a1a"
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
button_ventas = create_button(frame_data, "Ventas", active_ventas)
button_ventas.grid(row=1, column=0, padx=0)

button_inventario = create_button(frame_data, "Inventario")
button_inventario.grid(row=1, column=1)

button_contabilidad = create_button(frame_data, "Contabilidad")
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

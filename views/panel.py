import customtkinter
import subprocess
import sys
import threading

from config import (
     LABEL_FONT,
     CHECKER_FONT,
     TITLE_FONT,
     COLOR_NEGRO,
     COLOR_GRIS,
     COLOR_ROJO_VINO
)
from customtkinter import (
     CTkLabel,
     CTkButton,
     CTkFrame,
     CTkTextbox,
     CTkTabview
)
from modulo_sistema import ModuloSistema
from mostrar_consola import steam_to_textbox
from terminar_subproceso import terminar_subproceso


# CREAR BOTONES
def create_button(app, desc):
     return CTkButton(
          app,
          text=desc,
          font=LABEL_FONT,
          width=150,
          height=100,
          fg_color=COLOR_ROJO_VINO,
          bg_color="transparent",
          hover_color="gray"
     )


# CERRAR APLICACIÓN Y TERMINAR SUBPROCESOS (INCLUIDO EL FRAMEWORK)
def on_closing():
     ventas.detener()
     inventario.detener()
     contabilidad.detener()

     global subproc_js
     subproc_js = terminar_subproceso(subproc_js)
     
     app.destroy()
     sys.exit()


# INICIAR APLICACIÓN
app = customtkinter.CTk()
app.protocol("WM_DELETE_WINDOW", on_closing)
app.geometry("800x500")
app.title("Panel de Control LegacyBridge")
customtkinter.set_appearance_mode("light")


# VENTANA PRINCIPAL
frame_data = CTkFrame(
     app,
     width=800,
     height=400,
     corner_radius=0
)
frame_data.pack(fill="both", expand=True)
frame_data.columnconfigure((0,1,2), weight=1)
frame_data.rowconfigure((0,1,2), weight=1)


# TÍTULO
CTkLabel(
     frame_data,
     text="PANEL DE CONTROL - GRUPO 4 (ARQUITECTURA DE SOFTWARE)",
     wraplength=500,
     font=TITLE_FONT,
     text_color=COLOR_NEGRO
).grid(row=0, column=0, columnspan=3)


# FRAME TAB PARA FUNCIONALIDADES (BOTONES DE SERVICIOS Y CONSOLA)
tab_options = CTkTabview(
     frame_data,
     width=800,
     height=300,
     corner_radius=10,
     segmented_button_selected_hover_color=COLOR_ROJO_VINO,
     segmented_button_unselected_hover_color=COLOR_GRIS,
     segmented_button_fg_color=COLOR_ROJO_VINO,
     segmented_button_selected_color=COLOR_ROJO_VINO,
     fg_color=COLOR_GRIS
)
tab_options.grid(row=1, column=0, columnspan=3, pady=20, padx=20, sticky="nsew")

tab1 = tab_options.add("SERVICIOS")
tab1.grid_rowconfigure((0,1), weight=1)
tab1.grid_columnconfigure((0,1,2), weight=1)
tab2 = tab_options.add("CONSOLA")


# SELECCIÓN DE SERVICIOS
CTkLabel(
     tab1,
     text="Seleccione un servicio para iniciar:",
     wraplength=500,
     font=CHECKER_FONT,
     text_color=COLOR_NEGRO
).grid(row=0, column=0, columnspan=3)


# BOTONES DE VENTAS, INVENTARIO Y CONTABILIDAD
button_ventas = create_button(tab1, "Ventas")
button_ventas.grid(row=1, column=0, padx=0)

button_inventario = create_button(tab1, "Inventario")
button_inventario.grid(row=1, column=1)

button_contabilidad = create_button(tab1, "3era opción")
button_contabilidad.grid(row=1, column=2)


# TEXTBOX PARA MOSTRAR MENSAJES DEL FRAMEWORK Y SUBPROCESOS
textbox_checker = CTkTextbox(
     tab2,
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


# HILOS PARA LEER STDOUT Y STDERR DEL FRAMEWORK
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
     "Wrapper Inventario",
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

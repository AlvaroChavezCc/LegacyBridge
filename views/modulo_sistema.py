import subprocess
import threading
from config import COLOR_VERDE, COLOR_ROJO_VINO
from terminar_subproceso import terminar_subproceso
from mostrar_consola import steam_to_textbox

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
               self.button.configure(fg_color=COLOR_ROJO_VINO)
               self.active = False

     def detener(self):
          self.subprocess = terminar_subproceso(self.subprocess)
          self.button.configure(fg_color=COLOR_ROJO_VINO)
          self.active = False

          if self.stdout_thread and self.stdout_thread.is_alive():
               self.stdout_thread.join(timeout=1)
          if self.stderr_thread and self.stderr_thread.is_alive():
               self.stderr_thread.join(timeout=1)
          self.stdout_thread = None
          self.stderr_thread = None


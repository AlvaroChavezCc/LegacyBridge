import subprocess

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
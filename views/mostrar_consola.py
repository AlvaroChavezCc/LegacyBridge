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
     
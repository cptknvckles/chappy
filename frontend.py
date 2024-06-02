import tkinter as tk
from tkinter import scrolledtext
#main window
root = tk.Tk()
root.title('Python Instant Messenger')
root.geometry('400x500')

#chat window
chat_disp = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', width=50, height=20)
chat_disp.pack(padx=10, pady=10)

#messege box
message_entry = tk.Entry(root, width=40)
message_entry.pack(padx=10, pady=5, side=tk.LEFT, expand=True, fill=tk.X)

send_button = tk.Button(root, text='Send')
send_button.pack(padx=10, pady=5, side=tk.RIGHT)


root.mainloop()
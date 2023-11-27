import tkinter as tk

def on_select(event):
    # Get selected line index
    index = listbox.curselection()[0]
    # Get the line's text
    selected_line = listbox.get(index)
    print(f"You selected: {selected_line}")

root = tk.Tk()
listbox = tk.Listbox(root)
listbox.bind('<<ListboxSelect>>', on_select)

# Add some items to the listbox
for i in range(10):
    listbox.insert(tk.END, f"Item {i}")

listbox.pack()
root.mainloop()
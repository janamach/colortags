import tkinter as tk
from tkinter import messagebox
import itertools
from datetime import datetime
from tkinter import simpledialog

class CustomDialog(simpledialog.Dialog):
    def body(self, master):
        self.title("Black or Brown?")
        tk.Button(master, text="black", command=lambda: self.ok("black")).grid(row=0)
        tk.Button(master, text="brown", command=lambda: self.ok("brown")).grid(row=1)

    def ok(self, answer):
        self.result = answer
        super().ok()

def on_select(event, output_file, selected_combinations):
    # Get the current line number
    line_num = event.widget.index('insert').split('.')[0]
    # Get the combination on the current line
    combination = event.widget.get(f'{line_num}.0', f'{line_num}.end')
    # If the combination is already selected, do nothing
    if combination in selected_combinations:
        return
    # Ask the user to choose between "Black", "Brown", and "Cancel". The user clicks
    # on one of the three buttons. The button "Brown" and "Black" store 
    # "Brown" and "Black" in the variable "answer". The button "Cancel" closes the
    # window.
    answer = CustomDialog(event.widget).result
    # If the user clicks on "Cancel", do nothing
    if answer == 'cancel':
        # Do not change the background color of the current line
        return
    # If the user clicks on "Black" or "Brown", append the combination and the answer
    # to a file
    else:
        with open(output_file, 'a') as file:
            file.write(f'{combination}, {answer},{datetime.now()}\n')
        # Change the background color of the current line to white
        event.widget.tag_add('selected', 'insert linestart', 'insert lineend')
        if answer == 'black':
            event.widget.tag_config('selected', background='gray')
        if answer == 'brown':
            event.widget.tag_config('selected', background='brown')
        # Append the combination and the current date to a file
        #with open(output_file, 'a') as file:
        #    file.write(f'{combination}, {datetime.now()}\n')
        # Make the current line unclickable
        event.widget.unbind('<Button-1>')
        # Add to the list of selected combinations
        selected_combinations.append(combination)

def open_main_window(button_text):
    global root
    root = tk.Tk()

    elements = ['O', 'B', 'G', 'V', 'Y']
    #combinations = [''.join(combination) for combination in itertools.permutations(elements, 3)]
    # Combinations include all options with 1-5 elements. Elements can repeat.
    # It can also include one, two, three, or four elements.
    # The elemenets are not uniuqe. 'oo' and 'OOO' is a valid combination.
    # The order of the elements is important. 'BO' and 'OB' are different combinations.
    # 'OO' is a valid combination.
    combinations = []
    for i in range(1, 5):

        #create all possible combinations of length i with non-unique elements
        combinations.extend([''.join(combination) for combination in itertools.product(elements, repeat=i)])


    # If there are no combinations, show a message box and quit
    if not combinations:
        messagebox.showinfo("Error", "There are no combinations")
        root.quit()
    #quit()

    color_map = {'O': 'orange', 'B': 'cyan', 'G': 'limegreen', 'V': 'violet', 'Y': 'yellow'}

    # Split the combinations based on the first character
    parts = {element: [combination for combination in combinations if combination.startswith(element)] for element in elements}

    # Read the first column of the output file and make those selections white in color and unclickable
    selected_combinations = []
    try:
        with open(f'{button_text}.csv', 'r') as file:
            selected_combinations = [line.split(',')[0] for line in file.readlines()]
    except FileNotFoundError:
        pass

    for column, element in enumerate(elements):
        text = tk.Text(root, width=4, font=("Helvetica", 22), bg=color_map[element])
        text.bind('<Button-1>', lambda event, output_file=f'{button_text}.csv', selected_combinations=selected_combinations: on_select(event, output_file, selected_combinations))
    
        for combination in parts[element]:
            text.insert('insert', combination + '\n')
            if combination in selected_combinations:
                text.tag_add('selected', 'end - 2 lines', 'end - 1 line')
                # Change the background color of the current line to selected_ant_color
                text.tag_config('selected', background="white")
    
        text.grid(column=column, row=0)

    root.mainloop()


def on_button_click(button_text):
    open_main_window(button_text)

    # Your existing code here...
    root.quit()

root = tk.Tk()

# Add three buttons at the start
button1 = tk.Button(root, text="Cr", command=lambda: on_button_click("Cr"))
button1.pack()

button2 = tk.Button(root, text="Ci17", command=lambda: on_button_click("Ci17"))
button2.pack()

button3 = tk.Button(root, text="Cancel", command=root.quit)
button3.pack()

root.mainloop()
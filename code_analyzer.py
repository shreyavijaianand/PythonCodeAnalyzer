import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import os
import subprocess
from radon.complexity import cc_visit

#defines a class that inherits from the tk.TK class (main 'blank canvas' window in a Tinker GUI)
class CodeAnalyzerApp(tk.Tk):
    #constructor method, new instance when the app is created
    def __init__(self):
        #creates the main window by calling the constructor of the parent class (tk.TK) and sets the title and size
        super().__init__()
        self.title("Code Analyzer")
        self.geometry("800x600")

        # creates a button that calls the open_file method when clicked. adds 10 pixels of vertical (y) padding
        open_btn = tk.Button(self, text="Open File", command=self.open_file)
        open_btn.pack(pady=10)

        # creates a textbox with vertical scrollbar for the report. sets size to window size and makes sure it resizes with window
        # wrap = tk.WORD makes text wrap at word boundaries.
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        # fill=tk.BOTH tells the text area to stretch horizontally and vertically. 
        # expand=True allows the text area to grow with the window
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # defines the color-coded text tags (if tag is used, format the text this way)
        self.text_area.tag_config('low', foreground='green')    # low complexity
        self.text_area.tag_config('medium', foreground='orange') # medium complexity
        self.text_area.tag_config('high', foreground='red')     # high complexity
        self.text_area.tag_config('style', foreground='purple') # style issues
    
    def open_file(self):
        # opens a file picker dialog and stores the file path of the opened file
        file_path = filedialog.askopenfilename(
            # allowed file types: .py
            title="Select a code file",
            filetypes=[
                ("Python files", "*.py")
            ]
        )
        # if user cancels or no file selected, function stops
        if not file_path:
            return
        
        # opens file and reads all contents into the string called 'code'
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file: {e}")
            return
        
        # clears text area (start to end) and writes the file name at the tope
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, f"Analysis for {os.path.basename(file_path)}:\n\n")

        # complexity analysis
        self.analyze_complexity(code)

        # style analysis
        self.analyze_style(file_path)
 

    def analyze_complexity(self, code):
        # write the section header in text area
        self.text_area.insert(tk.END, "Cyclomatic Complexity:\n")
        try:
            # use cc visit (gives you a list of all the functions and classes, with each one’s complexity score) to get complexity blocks
            blocks = cc_visit(code)
            # initialize a total comlexity counter
            total = 0
            # loops over each block and gets a complexity score
            for block in blocks:
                complexity = block.complexity
                # chooses color tag based on complexity level
                if complexity <= 5:
                    tag = 'low'
                elif complexity <= 10:
                    tag = 'medium'
                else:
                    tag = 'high'
                
                # formats the message, adds message with color tag, and adds complexity to total
                msg = f"{block.name} (line {block.lineno}): complexity {complexity}\n"
                self.text_area.insert(tk.END, msg, tag)
                total += complexity
            
            # calculate average complexity (avoid dividing by 0) and display it
            avg = total / len(blocks) if blocks else 0
            self.text_area.insert(
                tk.END,
                f"\nAverage complexity: {avg:.2f}\n\n"
            )
        except Exception as e:
            self.text_area.insert(tk.END, f"Error during complexity analysis: {e}\n\n")

    def analyze_style(self, file_path):
        # write the section header in text area
        self.text_area.insert(tk.END, "Style Issues (PEP8):\n")
        try:
            # run pycodestyle as subprocess (external command in terminal e.g.) to capture output
            # pycodestyle notes - has result.stdout (actual output with style issues), result.stderr (any error messages),
            # result.returncode shows status of file (0 means no errors; 1 no PEP8 style errors; 2 is other errors)
            result = subprocess.run(
                ["pycodestyle", file_path],
                capture_output=True,
                text=True
            )
            # strips all the whitespace
            output = result.stdout.strip()
            # display a no style issues message
            if not output:
                self.text_area.insert(tk.END, "No style issues found.\n")
            else:
                # color-code each style issue line - purple
                for line in output.splitlines():
                    self.text_area.insert(tk.END, line + "\n", 'style')
        # if pycodestyle isn't installed, tell the user how to install it
        except FileNotFoundError:
            self.text_area.insert(
                tk.END,
                "pycodestyle not found. Please install it with `pip3 install pycodestyle`.\n",
                'style'
            )
        # catch all message for errors
        except Exception as e:
            self.text_area.insert(tk.END, f"Error during style analysis: {e}\n")

# makes sure script is being run directly and not imported
if __name__ == "__main__":
    # create an instance of the CodeAnalyzerApp by running the init() method
    app = CodeAnalyzerApp()
    # starts the Tkinter event loop to keep the app running.
    # starts an endless loop that waits for the user to do something.
    app.mainloop()

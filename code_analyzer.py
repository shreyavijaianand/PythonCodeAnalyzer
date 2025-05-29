import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import os
import subprocess
from radon.complexity import cc_visit

class CodeAnalyzerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Code Analyzer")
        self.geometry("800x600")

        # Open File button
        open_btn = tk.Button(self, text="Open File", command=self.open_file)
        open_btn.pack(pady=10)

        # Scrolled text area for output
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Configure tags for color-coding
        self.text_area.tag_config('low', foreground='green')    # Low complexity
        self.text_area.tag_config('medium', foreground='orange') # Medium complexity
        self.text_area.tag_config('high', foreground='red')     # High complexity
        self.text_area.tag_config('style', foreground='purple') # Style issues

    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a code file",
            filetypes=[
                ("Python files", "*.py"),
                ("JavaScript files", "*.js"),
                ("All files", "*.*")
            ]
        )
        if not file_path:
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file: {e}")
            return

        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, f"Analysis for {os.path.basename(file_path)}:\n\n")

        # Complexity analysis for Python files
        if file_path.endswith('.py'):
            self.analyze_complexity(code)
        else:
            self.text_area.insert(tk.END, "Cyclomatic complexity analysis only supported for Python files.\n\n")

        # Style analysis for Python files
        if file_path.endswith('.py'):
            self.analyze_style(file_path)
        else:
            self.text_area.insert(tk.END, "Style analysis (PEP8) only supported for Python files.\n")

    def analyze_complexity(self, code):
        self.text_area.insert(tk.END, "Cyclomatic Complexity:\n")
        try:
            blocks = cc_visit(code)
            total = 0
            for block in blocks:
                complexity = block.complexity
                # Determine tag based on complexity level
                if complexity <= 5:
                    tag = 'low'
                elif complexity <= 10:
                    tag = 'medium'
                else:
                    tag = 'high'

                msg = f"{block.name} (line {block.lineno}): complexity {complexity}\n"
                self.text_area.insert(tk.END, msg, tag)
                total += complexity

            avg = total / len(blocks) if blocks else 0
            self.text_area.insert(
                tk.END,
                f"\nAverage complexity: {avg:.2f}\n\n"
            )
        except Exception as e:
            self.text_area.insert(tk.END, f"Error during complexity analysis: {e}\n\n")

    def analyze_style(self, file_path):
        self.text_area.insert(tk.END, "Style Issues (PEP8):\n")
        try:
            # Run pycodestyle as subprocess to capture output
            result = subprocess.run(
                ["pycodestyle", file_path],
                capture_output=True,
                text=True
            )
            output = result.stdout.strip()
            if not output:
                self.text_area.insert(tk.END, "No style issues found.\n")
            else:
                # Color-code each style issue line
                for line in output.splitlines():
                    self.text_area.insert(tk.END, line + "\n", 'style')
        except FileNotFoundError:
            self.text_area.insert(
                tk.END,
                "pycodestyle not found. Please install it with `pip install pycodestyle`.\n",
                'style'
            )
        except Exception as e:
            self.text_area.insert(tk.END, f"Error during style analysis: {e}\n")

if __name__ == "__main__":
    # Note: Requires installing dependencies:
    #   pip3 install radon pycodestyle

    # Then run using python3 code_analyzer_app.py
    app = CodeAnalyzerApp()
    app.mainloop()

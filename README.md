# Python Code Analyzer

A simple Python desktop app built with Tkinter that helps you analyze your code! This tool runs **Radon** to check for cyclomatic complexity and **pycodestyle** for PEP8 style issues, then displays color-coded results in a user-friendly interface.

---

## What does this project do? Who is it for?

This application is designed for:

- **Developers** who want to improve their code quality.
- **Anyone** writing Python files and curious about code complexity and style issues.

Simply upload a `.py` file, analyze it, and generate a report—all in one place!

---

## Key Features

- Open and analyze any `.py` code file.
- Check cyclomatic complexity using **Radon**.
- Identify PEP8 style violations with **pycodestyle**.
- See results in a scrollable text pane with color-coded highlights.

---

## Screenshot

![Report Example](https://github.com/user-attachments/assets/cd3d0bd6-68c1-41b5-a5c7-e5741d0b7564)

---

## Installation & Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-repo.git
    cd your-repo
    ```

2. Install required libraries:

    ```bash
    pip3 install radon pycodestyle
    ```

3. Run the application:

    ```bash
    python3 code_analyzer.py
    ```

---

## Prerequisites

- **Python 3.x** installed
- **radon** and **pycodestyle** libraries (installed via pip3 command above in Installation & Setup)
- **Tkinter** (should be included with Python, but may require separate setup on some systems)

> Currently tested on macOS. Contributions for Windows and Linux compatibility are welcome!

---

## Testing

- Includes `sample_test.py` for testing.
- The expected output (commented at the end of the file, starts at line 36) should match the generated report.

![Expected Output of the Provided Test File](https://github.com/user-attachments/assets/3136c809-cb7f-4e17-9a1c-6e4559aad20b)

---

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

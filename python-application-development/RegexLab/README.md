# RegexLab
A simple, fast, and cross-platform desktop GUI for testing Regular Expressions, built with Python and Tkinter.

## Features
- **Real-time Matching:** See matches highlighted instantly as you type.
- **Interactive Cheatsheet:** A collapsible sidebar with common regex patterns for quick reference.
- **Cross-Platform:** Works seamlessly on Windows, macOS, and Linux.
- **Smart Clipboard:** Full support for shortcuts (Ctrl/Cmd+C, V, X, Z, Y) across different keyboard layouts.
- **Newline Handling:** Automatically converts `\n` to real newlines when pasting test strings, and real newlines to `\n` in the regex input.
- **Error Handling:** Highlights the input in red and displays a helpful error message for invalid patterns.

## Requirements
- Python 3.10 or higher (No external dependencies required, uses built-in `tkinter`).

## Getting Started
To run the application locally, clone the project folder:
```bash
git clone --filter=blob:none --no-checkout https://github.com/510o/HsoubAcademy.git
cd HsoubAcademy
git sparse-checkout init --cone
git sparse-checkout set python-application-development/RegexLab
git checkout main
cd python-application-development/RegexLab
```
Then, start the app:
```bash
python main.py
```

## License
MIT
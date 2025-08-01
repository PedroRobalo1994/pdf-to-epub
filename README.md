# PDF to EPUB Converter

This script converts PDF files to EPUB format, preserving images, text, and vector graphics. It can be run from the command line or with a graphical user interface (GUI) that supports drag-and-drop.

## Features

-   **PDF to EPUB Conversion:** Converts PDF files to EPUB format.
-   **Image and Text Preservation:** Retains images and text from the original PDF.
-   **Vector Graphics Support:** Preserves vector graphics, such as charts and graphs.
-   **Command-Line Interface (CLI):** Allows for batch processing and integration with other scripts.
-   **Graphical User Interface (GUI):** Provides an easy-to-use interface for converting files.
-   **Drag-and-Drop:** Supports dragging and dropping PDF files directly into the GUI.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/<your-username>/pdf-to-epub.git
    cd pdf-to-epub
    ```

2.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### GUI Mode

To run the application in GUI mode, simply execute the script without any arguments:

```bash
python converter.py
```

This will open a window where you can either browse for a PDF file or drag and drop it into the application. After selecting a file, click the "Convert to EPUB" button to save the converted file.

### Command-Line Mode

To run the application in command-line mode, use the `--no-gui` flag and specify the input and output file paths:

```bash
python converter.py --no-gui --input /path/to/your/file.pdf --output /path/to/your/file.epub
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or find any bugs.


import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox
from ebooklib import epub
from PIL import Image
import io
import os
import argparse
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD

class PDFToEPUBConverter:
    def __init__(self, gui=True):
        if gui:
            self.init_gui()

    def convert_to_epub(self, pdf_path, epub_path):
        try:
            doc = fitz.open(pdf_path)
            book = epub.EpubBook()

            # Set metadata
            if doc.metadata:
                if doc.metadata.get("title"):
                    book.set_title(doc.metadata["title"])
                if doc.metadata.get("author"):
                    book.add_author(doc.metadata["author"])

            book.set_language("en")

            items = []
            for i, page in enumerate(doc):
                # Extract text
                text = page.get_text("html")

                # Extract images
                img_list = page.get_images(full=True)
                for img_index, img in enumerate(img_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    image_filename = f"image{i}_{img_index}.{image_ext}"
                    
                    # Add image to epub
                    epub_image = epub.EpubImage(
                        uid=f"img_{i}_{img_index}",
                        file_name=f"images/{image_filename}",
                        media_type=f"image/{image_ext}",
                        content=image_bytes,
                    )
                    book.add_item(epub_image)
                    
                    # Replace image placeholder in text
                    text = text.replace(f'''<img src="images/image{i}_{img_index}.{image_ext}" alt=""/>''', f'''<img src="{epub_image.file_name}" alt=""/>''')


                # Create chapter
                chapter = epub.EpubHtml(
                    title=f"Page {i+1}",
                    file_name=f"page_{i+1}.xhtml",
                    lang="en",
                )
                chapter.content = text
                book.add_item(chapter)
                items.append(chapter)

            # Define Table of Contents
            book.toc = (items)

            # Add default NCX and Nav file
            book.add_item(epub.EpubNcx())
            book.add_item(epub.EpubNav())

            # Define CSS style
            style = "BODY {color: black;}"
            nav_css = epub.EpubItem(
                uid="style_nav",
                file_name="style/nav.css",
                media_type="text/css",
                content=style,
            )
            book.add_item(nav_css)

            # Create spine
            book.spine = ["nav"] + items

            # Create epub file
            epub.write_epub(epub_path, book, {})
            if hasattr(self, 'status_label'):
                self.status_label.configure(text=f"Successfully converted to {os.path.basename(epub_path)}")
            else:
                print(f"Successfully converted to {epub_path}")

        except Exception as e:
            if hasattr(self, 'status_label'):
                self.status_label.configure(text=f"Error: {e}")
            else:
                print(f"Error: {e}")


    def init_gui(self):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.root = TkinterDnD.Tk()
        self.root.title("PDF to EPUB Converter")
        self.root.geometry("500x350")

        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.label = ctk.CTkLabel(self.frame, text="Drag and Drop PDF Here or", font=("Arial", 16))
        self.label.pack(pady=10)

        self.browse_button = ctk.CTkButton(self.frame, text="Browse for PDF", command=self.browse_file)
        self.browse_button.pack(pady=10)

        self.file_label = ctk.CTkLabel(self.frame, text="No file selected", text_color="gray")
        self.file_label.pack(pady=10)

        self.convert_button = ctk.CTkButton(self.frame, text="Convert to EPUB", command=self.convert_gui, state="disabled")
        self.convert_button.pack(pady=20)
        
        self.status_label = ctk.CTkLabel(self.frame, text="", font=("Arial", 12))
        self.status_label.pack(pady=5)

        self.pdf_path = None

        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.drop)

    def browse_file(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.pdf_path:
            self.file_label.configure(text=os.path.basename(self.pdf_path))
            self.convert_button.configure(state="normal")

    def drop(self, event):
        self.pdf_path = event.data.strip('{}')
        if self.pdf_path.lower().endswith(".pdf"):
            self.file_label.configure(text=os.path.basename(self.pdf_path))
            self.convert_button.configure(state="normal")
        else:
            self.file_label.configure(text="Please drop a PDF file.", text_color="red")

    def convert_gui(self):
        if self.pdf_path:
            epub_path = filedialog.asksaveasfilename(defaultextension=".epub", filetypes=[("EPUB files", "*.epub")])
            if epub_path:
                self.status_label.configure(text="Converting...")
                self.convert_to_epub(self.pdf_path, epub_path)

def main():
    parser = argparse.ArgumentParser(description="Convert a PDF file to EPUB format.")
    parser.add_argument("-i", "--input", help="Input PDF file path.")
    parser.add_argument("-o", "--output", help="Output EPUB file path.")
    parser.add_argument("--no-gui", help="Run in command-line mode without GUI.", action="store_true")

    args = parser.parse_args()

    if args.no_gui:
        if not args.input or not args.output:
            print("Error: Both --input and --output are required for command-line mode.")
            return
        converter = PDFToEPUBConverter(gui=False)
        converter.convert_to_epub(args.input, args.output)
    else:
        # If input and output are provided, run in CLI mode, otherwise launch GUI
        if args.input and args.output:
            converter = PDFToEPUBConverter(gui=False)
            converter.convert_to_epub(args.input, args.output)
        else:
            app = PDFToEPUBConverter(gui=True)
            app.root.mainloop()

if __name__ == "__main__":
    main()

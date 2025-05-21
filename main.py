import os
import fitz
import re
from openpyxl import Workbook
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog

root = tk.Tk()
root.withdraw()

def seleccionar_pdfs_o_carpeta():
    class SelectorDialog(tk.Toplevel):
        def __init__(self, parent):
            super().__init__(parent)
            self.title("Importar archivos PDF")
            self.res = None
            tk.Label(self, text="¿Cómo desea importar los archivos PDF?").pack(padx=20, pady=(15, 10))
            btn_frame = tk.Frame(self)
            btn_frame.pack(pady=(0, 15))
            tk.Button(btn_frame, text="Seleccionar archivos", width=20, command=self.select_files).pack(side=tk.LEFT, padx=10)
            tk.Button(btn_frame, text="Seleccionar carpeta", width=20, command=self.select_folder).pack(side=tk.LEFT, padx=10)
            self.protocol("WM_DELETE_WINDOW", self.cancel)
        def select_files(self):
            self.res = "files"
            self.destroy()
        def select_folder(self):
            self.res = "folder"
            self.destroy()
        def cancel(self):
            self.res = None
            self.destroy()
    root = tk.Tk()
    root.withdraw()
    root.deiconify()
    dialog = SelectorDialog(root)
    root.wait_window(dialog)
    choice = dialog.res
    root.withdraw()
    pdf_paths = []
    if choice == "files":
        files = filedialog.askopenfilenames(
            title="Seleccionar archivos PDF",
            filetypes=[("Archivos PDF", "*.pdf")],
        )
        pdf_paths = list(files)
    elif choice == "folder":
        folder = filedialog.askdirectory(title="Seleccionar carpeta con PDFs")
        if folder:
            pdf_paths = [
                os.path.join(folder, f)
                for f in os.listdir(folder)
                if f.lower().endswith(".pdf") and os.path.isfile(os.path.join(folder, f))
            ]
    if not pdf_paths:
        messagebox.showinfo("Sin selección", "No se seleccionaron archivos PDF. Saliendo.")
        exit()
    return pdf_paths, root

pdf_files, root = seleccionar_pdfs_o_carpeta()

excel_filename = simpledialog.askstring("Nombre de archivo", "Ingrese el nombre del archivo Excel (sin extensión):")
if not excel_filename:
    excel_filename = "resultados"
excel_filename += ".xlsx"

class KeywordDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Palabras clave")
        self.keywords = []
        self.result = None
        tk.Label(self, text="Ingrese la palabra clave a buscar:").pack(padx=10, pady=(10, 2))
        self.entry = tk.Entry(self, width=40)
        self.entry.pack(padx=10, pady=2)
        self.entry.focus()
        frame = tk.Frame(self)
        frame.pack(pady=10)
        tk.Button(frame, text="Siguiente", command=self.add_keyword).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Listo", command=self.finish).pack(side=tk.LEFT, padx=5)
        self.protocol("WM_DELETE_WINDOW", self.finish)
    def add_keyword(self):
        palabra = self.entry.get().strip()
        if palabra:
            self.keywords.append(palabra)
            self.entry.delete(0, tk.END)
            self.entry.focus()
    def finish(self):
        palabra = self.entry.get().strip()
        if palabra:
            self.keywords.append(palabra)
        self.result = self.keywords
        self.destroy()

root.deiconify()
dialog = KeywordDialog(root)
root.wait_window(dialog)
keywords = dialog.result if dialog.result else []
root.withdraw()

if not keywords:
    messagebox.showinfo("Sin palabras clave", "No se ingresaron palabras clave. Saliendo.")
    exit()

all_results = []

for pdf_path in pdf_files:
    filename = os.path.basename(pdf_path)
    with fitz.open(pdf_path) as pdf:
        text = ""
        for page in pdf:
            text += page.get_text() + "\n"
        results = {}
        for kw in keywords:
            kw_clean = kw.rstrip(":").strip()
            pattern = rf"\b{re.escape(kw_clean)}\b:?\s*([^\w\d]*)([A-Za-z0-9].*)"
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                results[kw] = match.group(2).strip()
            else:
                results[kw] = "No encontrado"
    row = [filename] + [results[kw] for kw in keywords]
    all_results.append(row)

if all_results:
    wb = Workbook()
    ws = wb.active
    ws.title = "Resultados"
    ws.append(["Archivo"] + keywords)
    for row in all_results:
        ws.append(row)
    resultados_folder = os.path.join(os.path.dirname(__file__), "resultados")
    os.makedirs(resultados_folder, exist_ok=True)
    excel_path = os.path.join(resultados_folder, excel_filename)
    wb.save(excel_path)
    messagebox.showinfo("Éxito", "Excel exportado con éxito")




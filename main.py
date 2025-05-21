import os
import fitz
import re
from openpyxl import Workbook
import tkinter as tk
from tkinter import simpledialog, messagebox

pdf_folder = "archivos_pdf"

root = tk.Tk()
root.withdraw()

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

for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        with fitz.open(pdf_path) as pdf:
            text = pdf[0].get_text()
            results = {}
            for kw in keywords:
                match = re.search(rf"{re.escape(kw)}\s*(.*)", text)
                results[kw] = match.group(1).strip() if match else "No encontrado"
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




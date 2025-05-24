import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog

def get_tk_root():
    root = tk.Tk()
    root.withdraw()
    return root

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
    root = get_tk_root()
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

def pedir_nombre_excel(root):
    excel_filename = simpledialog.askstring("Nombre de archivo", "Ingrese el nombre del archivo Excel (sin extensión):", parent=root)
    if not excel_filename:
        excel_filename = "resultados"
    return excel_filename + ".xlsx"

def pedir_palabras_clave(root):
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
    return keywords

def mostrar_info(titulo, mensaje):
    messagebox.showinfo(titulo, mensaje)

class MultiSelectDialog(tk.Toplevel):
    def __init__(self, parent, keyword, matches):
        super().__init__(parent)
        self.title(f"Seleccionar para '{keyword}'")
        self.selected = []
        tk.Label(self, text=f"Seleccione los resultados para '{keyword}':").pack(padx=10, pady=(10, 2))
        self.vars = []
        for match in matches:
            var = tk.BooleanVar(value=False)
            cb = tk.Checkbutton(self, text=match, variable=var, anchor="w", justify="left")
            cb.pack(fill="x", padx=10, anchor="w")
            self.vars.append((var, match))
        tk.Button(self, text="OK", command=self.finish).pack(pady=10)
        self.protocol("WM_DELETE_WINDOW", self.finish)
    def finish(self):
        self.selected = [match for var, match in self.vars if var.get()]
        self.destroy()

import os
import customtkinter as ctk
from tkinter import filedialog, messagebox

def get_tk_root():
    root = ctk.CTk()
    root.withdraw()
    return root

def seleccionar_pdfs_o_carpeta():
    class SelectorDialog(ctk.CTkToplevel):
        def __init__(self, parent):
            super().__init__(parent)
            self.title("Importar archivos PDF")
            self.res = None
            self.geometry("400x180")
            ctk.CTkLabel(self, text="¿Cómo desea importar los archivos PDF?", font=ctk.CTkFont(size=16, weight="bold")).pack(padx=20, pady=(20, 10))
            btn_frame = ctk.CTkFrame(self)
            btn_frame.pack(pady=(0, 15))
            ctk.CTkButton(btn_frame, text="Seleccionar archivos", width=160, command=self.select_files).pack(side="left", padx=10)
            ctk.CTkButton(btn_frame, text="Seleccionar carpeta", width=160, command=self.select_folder).pack(side="left", padx=10)
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
    excel_filename = ctk.CTkInputDialog(text="Ingrese el nombre del archivo Excel (sin extensión):", title="Nombre de archivo").get_input()
    if not excel_filename:
        excel_filename = "resultados"
    return excel_filename + ".xlsx"

def pedir_palabras_clave(root):
    class KeywordDialog(ctk.CTkToplevel):
        def __init__(self, parent):
            super().__init__(parent)
            self.title("Palabras clave")
            self.geometry("420x320")
            self.keywords = []
            self.result = None
            ctk.CTkLabel(self, text="Ingrese las palabras clave a buscar", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 10))
            entry_frame = ctk.CTkFrame(self)
            entry_frame.pack(pady=5)
            self.entry = ctk.CTkEntry(entry_frame, width=220, placeholder_text="Ej: paciente")
            self.entry.pack(side="left", padx=(0,10))
            ctk.CTkButton(entry_frame, text="Agregar", width=80, command=self.add_keyword).pack(side="left")
            self.keywords_box = ctk.CTkTextbox(self, height=100, width=340)
            self.keywords_box.pack(pady=10)
            self.keywords_box.configure(state="disabled")
            btn_frame = ctk.CTkFrame(self)
            btn_frame.pack(pady=10)
            ctk.CTkButton(btn_frame, text="Listo", width=100, command=self.finish).pack(side="left", padx=10)
            ctk.CTkButton(btn_frame, text="Cancelar", width=100, command=self.cancel).pack(side="left", padx=10)
            self.protocol("WM_DELETE_WINDOW", self.cancel)
            self.entry.bind("<Return>", lambda e: self.add_keyword())
        def add_keyword(self):
            palabra = self.entry.get().strip()
            if palabra and palabra not in self.keywords:
                self.keywords.append(palabra)
                self.entry.delete(0, "end")
                self.keywords_box.configure(state="normal")
                self.keywords_box.insert("end", palabra + "\n")
                self.keywords_box.configure(state="disabled")
        def finish(self):
            self.result = self.keywords
            self.destroy()
        def cancel(self):
            self.result = []
            self.destroy()
    root.deiconify()
    dialog = KeywordDialog(root)
    root.wait_window(dialog)
    keywords = dialog.result if dialog.result else []
    root.withdraw()
    return keywords

def mostrar_info(titulo, mensaje):
    messagebox.showinfo(titulo, mensaje)

class MultiSelectDialog(ctk.CTkToplevel):
    def __init__(self, parent, keyword, matches):
        super().__init__(parent)
        self.title(f"Seleccionar para '{keyword}'")
        self.geometry("500x350")
        self.selected = []
        ctk.CTkLabel(self, text=f"Seleccione los resultados para '{keyword}':", font=ctk.CTkFont(size=15, weight="bold")).pack(padx=10, pady=(15, 8))
        self.vars = []
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=5)
        for match in matches:
            var = ctk.BooleanVar(value=False)
            cb = ctk.CTkCheckBox(frame, text=match, variable=var, font=ctk.CTkFont(size=13))
            cb.pack(anchor="w", padx=10, pady=2)
            self.vars.append((var, match))
        ctk.CTkButton(self, text="OK", width=120, command=self.finish).pack(pady=15)
        self.protocol("WM_DELETE_WINDOW", self.finish)
    def finish(self):
        self.selected = [match for var, match in self.vars if var.get()]
        self.destroy()

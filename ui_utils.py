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
            self.geometry("420x340")
            self.keywords = []
            self.result = None
            ctk.CTkLabel(self, text="Ingrese las palabras clave a buscar", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 10))
            entry_frame = ctk.CTkFrame(self)
            entry_frame.pack(pady=5)
            self.entry = ctk.CTkEntry(entry_frame, width=220, placeholder_text="Ej: paciente")
            self.entry.pack(side="left", padx=(0,10))
            ctk.CTkButton(entry_frame, text="Agregar", width=80, command=self.add_keyword).pack(side="left")
            # Contenedor dinámico para palabras clave
            self.keywords_container = ctk.CTkFrame(self)
            self.keywords_container.pack(pady=10, fill="x")
            btn_frame = ctk.CTkFrame(self)
            btn_frame.pack(pady=10)
            ctk.CTkButton(btn_frame, text="Listo", width=100, command=self.finish).pack(side="left", padx=10)
            ctk.CTkButton(btn_frame, text="Cancelar", width=100, command=self.cancel).pack(side="left", padx=10)
            self.status = ctk.CTkLabel(self, text="", text_color="red")
            self.status.pack(pady=5)
            self.protocol("WM_DELETE_WINDOW", self.cancel)
            self.entry.bind("<Return>", lambda e: self.add_keyword())
            self.keyword_widgets = {}  # palabra: frame

        def add_keyword(self):
            palabra = self.entry.get().strip()
            if palabra and palabra not in self.keywords:
                self.keywords.append(palabra)
                self.entry.delete(0, "end")
                self._add_keyword_widget(palabra)
                self.status.configure(text="")
            elif palabra in self.keywords:
                self.status.configure(text="La palabra ya fue agregada.")

        def _add_keyword_widget(self, palabra):
            kw_frame = ctk.CTkFrame(self.keywords_container)
            kw_frame.pack(fill="x", pady=2, padx=5)
            lbl = ctk.CTkLabel(kw_frame, text=palabra, anchor="w")
            lbl.pack(side="left", padx=(5, 2), fill="x", expand=True)
            btn = ctk.CTkButton(kw_frame, text="❌", width=30, fg_color="#d9534f", hover_color="#c9302c", command=lambda: self.remove_keyword(palabra))
            btn.pack(side="right", padx=2)
            self.keyword_widgets[palabra] = kw_frame

        def remove_keyword(self, palabra):
            if palabra in self.keywords:
                self.keywords.remove(palabra)
            if palabra in self.keyword_widgets:
                self.keyword_widgets[palabra].destroy()
                del self.keyword_widgets[palabra]

        def finish(self):
            if not self.keywords:
                self.status.configure(text="Debes ingresar al menos una palabra clave.")
                return
            self.result = list(self.keywords)
            self.after(1, self.destroy)

        def cancel(self):
            self.result = []
            self.after(1, self.destroy)

    root.deiconify()
    dialog = KeywordDialog(root)
    dialog.update()
    while True:
        root.update()
        if not dialog.winfo_exists():
            break
    keywords = dialog.result if dialog.result is not None else []
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

from ui_utils import (
    seleccionar_pdfs_o_carpeta,
    pedir_nombre_excel,
    pedir_palabras_clave,
    mostrar_info,
    MultiSelectDialog,
    get_tk_root,
)
from pdf_utils import extraer_resultados_pdf
from openpyxl import Workbook
import os
import tkinter as tk

def main():
    pdf_files, root = seleccionar_pdfs_o_carpeta()
    excel_filename = pedir_nombre_excel(root)
    keywords = pedir_palabras_clave(root)
    if not keywords:
        mostrar_info("Sin palabras clave", "No se ingresaron palabras clave. Saliendo.")
        return

    all_results = []
    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        resultados = extraer_resultados_pdf(
            pdf_path, keywords, root, MultiSelectDialog
        )
        row = [filename] + [resultados[kw] for kw in keywords]
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
        mostrar_info("Éxito", "Excel exportado con éxito")

if __name__ == "__main__":
    main()




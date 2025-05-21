import os
import fitz  # PyMuPDF
import re
from openpyxl import Workbook

# Ruta de la carpeta con los PDF
pdf_folder = "archivos_pdf"

# Pedir al usuario el nombre del archivo Excel
excel_filename = input("Ingrese el nombre del archivo Excel (sin extensión): ").strip()
if not excel_filename:
    excel_filename = "resultados"
excel_filename += ".xlsx"

# Pedir al usuario las palabras clave a buscar
keywords = []
print("Ingrese las palabras clave a buscar (escriba '1' para terminar):")
while True:
    palabra = input("Palabra clave: ").strip()
    if palabra == "1":
        break
    if palabra:
        keywords.append(palabra)
if not keywords:
    print("No se ingresaron palabras clave. Saliendo.")
    exit()

# Lista para almacenar los resultados de todos los archivos
all_results = []

# Iterar sobre los archivos
for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)

        # Abrir el PDF
        with fitz.open(pdf_path) as pdf:
            first_page = pdf[0]  # primera página
            text = first_page.get_text()

            # Diccionario para guardar los resultados
            results = {}

            for kw in keywords:
                # Buscar el texto a la derecha de la palabra clave
                # Busca la palabra clave seguida de cualquier cantidad de espacios y luego captura el texto hasta el final de la línea
                match = re.search(rf"{re.escape(kw)}\s*(.*)", text)
                if match:
                    results[kw] = match.group(1).strip()
                else:
                    results[kw] = "No encontrado"

        print(f"Archivo: {filename}")
        for kw in keywords:
            print(f"  {kw} {results[kw]}")

        # Agregar resultados a la lista
        row = [filename] + [results[kw] for kw in keywords]
        all_results.append(row)

# Guardar los resultados en un archivo Excel
if all_results:
    wb = Workbook()
    ws = wb.active
    ws.title = "Resultados"
    # Escribir encabezados
    ws.append(["Archivo"] + keywords)
    # Escribir datos
    for row in all_results:
        ws.append(row)
    # Guardar el archivo en la carpeta 'resultados'
    resultados_folder = os.path.join(os.path.dirname(__file__), "resultados")
    os.makedirs(resultados_folder, exist_ok=True)
    excel_path = os.path.join(resultados_folder, excel_filename)
    wb.save(excel_path)
    print(f"\nResultados guardados en: {excel_path}")




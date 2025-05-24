import fitz
import re

def extraer_resultados_pdf(pdf_path, keywords, root, MultiSelectDialog):
    with fitz.open(pdf_path) as pdf:
        text = ""
        for page in pdf:
            text += page.get_text() + "\n"
        results = {}
        for kw in keywords:
            kw_clean = kw.rstrip(":").strip()
            pattern = rf"\b{re.escape(kw_clean)}\b:?\s*([^\w\d]*)([A-Za-z0-9][^\n]*)"
            matches = re.findall(pattern, text, re.IGNORECASE)
            found = [m[1].strip() for m in matches if m[1].strip()]
            if not found:
                results[kw] = "No encontrado"
            elif len(found) == 1:
                results[kw] = found[0]
            else:
                root.deiconify()
                dialog = MultiSelectDialog(root, kw, found)
                root.wait_window(dialog)
                selected = dialog.selected if dialog.selected is not None else []
                root.withdraw()
                if selected:
                    results[kw] = "; ".join(selected)
                else:
                    results[kw] = "No seleccionado"
    return results

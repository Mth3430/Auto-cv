import json
import os
import shutil
import typst

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "letter_template.typ")

def export_letter(letter_data, output_pdf):
    folder = os.path.dirname(output_pdf)
    os.makedirs(folder, exist_ok=True)

    data_path = os.path.join(folder, "letter_data.json")
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(letter_data, f, ensure_ascii=False, indent=2)

    typ_path = os.path.join(folder, "letter.typ")
    shutil.copy2(TEMPLATE_PATH, typ_path)

    typst.compile(typ_path, output=output_pdf)
    print(f"  [PDF] Lettre générée : {output_pdf}")

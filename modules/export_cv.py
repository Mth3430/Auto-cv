import json
import os
import shutil
import typst

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "cv_template.typ")

def export_cv(cv_data, output_pdf):
    folder = os.path.dirname(output_pdf)
    os.makedirs(folder, exist_ok=True)

    # Resolve photo path to absolute so Typst can find it
    photo = cv_data.get("photo", "")
    if photo and not os.path.isabs(photo):
        photo = os.path.abspath(photo)
    if photo and os.path.isfile(photo):
        # Copy photo next to the .typ file so the relative path works
        dest = os.path.join(folder, "photo" + os.path.splitext(photo)[1])
        shutil.copy2(photo, dest)
        cv_data["photo"] = os.path.basename(dest)
    else:
        cv_data["photo"] = ""

    # Write data JSON next to output
    data_path = os.path.join(folder, "cv_data.json")
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(cv_data, f, ensure_ascii=False, indent=2)

    # Copy template next to data so relative paths resolve
    typ_path = os.path.join(folder, "cv.typ")
    shutil.copy2(TEMPLATE_PATH, typ_path)

    # Compile
    typst.compile(typ_path, output=output_pdf)
    print(f"  [PDF] CV généré : {output_pdf}")

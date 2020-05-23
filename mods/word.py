import sys
import json
import subprocess
from pathlib import Path
from tqdm.auto import tqdm

def convert(paths, keep_active):
    import win32com.client

    word = win32com.client.Dispatch("Word.Application")
    wdFormatPDF = 17

    if paths["batch"]:
        for docx_filepath in tqdm(sorted(Path(paths["input"]).glob("*.docx"))):
            pdf_filepath = Path(paths["output"]) / (str(docx_filepath.stem) + ".pdf")
            doc = word.Documents.Open(str(docx_filepath))
            doc.SaveAs(str(pdf_filepath), FileFormat=wdFormatPDF)
            doc.Close()
    else:
        pbar = tqdm(total=1)
        docx_filepath = Path(paths["input"]).resolve()
        pdf_filepath = Path(paths["output"]).resolve()
        doc = word.Documents.Open(str(docx_filepath))
        doc.SaveAs(str(pdf_filepath), FileFormat=wdFormatPDF)
        doc.Close()
        pbar.update(1)

    if not keep_active:
        word.Quit()
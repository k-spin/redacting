import pymupdf
import os
import pathlib
import tkinter as tk
from tkinter import filedialog

def select_files() -> tuple[list[pathlib.Path],list[pathlib.Path]]:

    pdfdir = 'docs_to_write_on'
    jsondir = 'jsons_to_read'

    root = tk.Tk()
    root.withdraw()

    # NOTE: check to see if this can be changed to selecting entire folder (and include also all subfolders)
    pdf_files = filedialog.askopenfilenames(initialdir=os.getcwd() +"\\"+ pdfdir, title="Select PDF for marking",
                                            filetypes=[("PDF Files", "*.pdf")])
    pdf_files = {pathlib.Path(pa).stem:pathlib.Path(pa) for pa in pdf_files}


    # remove this later, this is only to select correct jsons now, when marker works in-system selecting JSONS won't be needed)
    json_files = {name:pathlib.Path(str(pa.parents[1])+"\\"+jsondir+"\\"+pa.stem+".json") for name,pa in pdf_files.items() if os.path.isfile(pathlib.Path(str(pa.parents[1])+"\\"+jsondir+"\\"+pa.stem+".json"))}


    verificationset = {pa.stem for name,pa in pdf_files.items()}.symmetric_difference({jpa.stem for jname,jpa in json_files.items()})
    if verificationset != set():
        print(verificationset)
        raise Exception(f"Some PDF files don't have corresponding JSON files: {verificationset}")
    
    
    return (pdf_files,json_files)

def check_ok_for_marker(filename: pathlib.Path) -> None :
    
    doc = pymupdf.open(filename)

    if not doc.can_save_incrementally():

        print(f'File: "{filename.stem}" unwritable. Fixing...')

        new_file = str(filename.parent) + filename.stem + "-fixed" + ".pdf"
        doc.save(new_file, garbage=4,deflate=True)
        doc.close()
        page=None
        os.remove(filename)
        os.rename(new_file,filename)
    else:
        print('Nothing to fix!')
import os
import pymupdf
import re


def bbox_to_coords(bbox: list) -> list:
   return [(bbox[0],bbox[1]),(bbox[2],bbox[1]),(bbox[2],bbox[3]),(bbox[0],bbox[3])]

def check_ok_to_write(filename):
    
    doc = pymupdf.open(filename)

    if not doc.can_save_incrementally():

        print(f'File: "{filename.stem}" unwritable. Fixing...')

        new_file = str(filename.parent) + filename.stem + "-fixed" + ".pdf"
        doc.save(new_file, garbage=4,deflate=True)
        doc.close()
        page=None
        os.remove(filename)
        os.rename(new_file,filename)
        doc = pymupdf.open(filename)
        return doc
    else:
        print('Nothing to fix!')
        return doc


def redact_handwriting(filename, redactions):

  doc = check_ok_to_write(filename)
  
  for i,page in enumerate(doc):
    lines = redactions[i]
    nredactions = len(lines)
    for ncoord,coords in enumerate(lines):
      print(f"Page {i}: Adding annotation {ncoord} / {nredactions}",end='\r')
      annot = page.add_redact_annot(coords,fill=(0,0,0))
      annot.update()
    page.apply_redactions()
    doc.saveIncr()
  doc.close()
  page=None
  print(f'"{filename.stem}" annotated.')



def add_boxes(filename, annotations):

  doc = check_ok_to_write(filename)
  
  for i,page in enumerate(doc):

    lines = annotations[i]
    nannots = len(lines)
    for ncoord,coords in enumerate(lines):
      print(f"Page {i}: Adding annotation {ncoord} / {nannots}",end='\r')
      annot = page.add_polygon_annot(bbox_to_coords(coords))
      annot.set_colors(stroke=(0.0431, 0.5882, 0.2509))
      annot.update()
      doc.saveIncr()
  doc.close()
  page=None
  print(f'"{filename.stem}" annotated.')
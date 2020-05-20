import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from PyPDF2 import PdfFileWriter, PdfFileReader
import PyPDF2
from PIL import Image


def save_pdf(data,path):
    with open(path,'wb') as f:
        f.write(data.read())


def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, 
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
            
        text = fake_file_handle.getvalue()
    
    # close open handles
    converter.close()
    fake_file_handle.close()
    
    if text:
        return text
    
def extract_images_from_pdf(pdf_path):
    pass

def convert_to_html(pdf_path, html_filename):
    pass

def split_pages(pdf_path, page_range, out_file):
   
    output = PdfFileWriter()
    input_pdf = PdfFileReader(open(pdf_path, "rb"))
    output_file = open(out_file, "wb")


    page_ranges = (x.split("-") for x in page_range.split(","))
    range_list = [i for r in page_ranges for i in range(int(r[0]), int(r[-1]) + 1)]

    for p in range_list:
        # Need to subtract 1 because pages are 0 indexed
        try:
            output.addPage(input_pdf.getPage(p - 1))
        except IndexError:
            # Alert the user and stop adding pages
            print("Range exceeded number of pages in input.\nFile will still be saved.")
            break
    output.write(output_file)

def getinfo(pdf_path):
    PDFfile=open(pdf_path,"rb")
    pdfread=PyPDF2.PdfFileReader(PDFfile)
    info=pdfread.getDocumentInfo()
    return info

def photo_to_pdf(images):
    img1=Image.open("images/task.jpg")
    img1.save("photos_pdf.pdf",'PDF',resolution=100,save_all=True,append_images=[images])


from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams, LTTextBox 
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfdevice import PDFDevice
import io
import pdfminer
import unicodedata


class ParsePdfClass:
    def __init__(self, path):
        self.path = path

    jsonScript = {
        "pdf": []
    }

    def parsepdf(self):
        # Open a PDF file.
        fp = open(self.path, 'rb')

        # Create a PDF parser object associated with the file object.
        parser = PDFParser(fp)

        # Create a PDF document object that stores the document structure.
        document = PDFDocument(parser)

        # Check if the document allows text extraction. If not, abort.
        if not document.is_extractable:
            return print("wrong format")

        # Create a PDF resource manager object that stores shared resources.
        rsrcmgr = PDFResourceManager()

        # Create a PDF device object.
        device = PDFDevice(rsrcmgr)

        # BEGIN LAYOUT ANALYSIS
        # Set parameters for analysis.
        laparams = LAParams(word_margin=100, boxes_flow=0.8)

        # Create a PDF page aggregator object.
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)

            # Create a PDF interpreter object.
        interpreter = PDFPageInterpreter(rsrcmgr, device)


        i = 0
        # loop over all pages in the document
        for page in PDFPage.create_pages(document):
            self.jsonScript["pdf"].append({
                "page": i,
                "content": []
            }) 
            
            # read the page into a layout object
            interpreter.process_page(page)
            layout = device.get_result()

            # extract text from this object
            self.parse_obj(layout._objs, page.mediabox[3])
            i += 1

    def parse_obj(self, lt_objs, pageHeight):

        # loop over the object list
        for obj in lt_objs:
            if isinstance(obj, pdfminer.layout.LTTextLine):
                # print(obj.bbox)
                self.jsonScript["pdf"][-1]["content"].append({
                    "x": obj.bbox[0],
                    "y": pageHeight - obj.bbox[1],
                    "text": obj.get_text().replace('\n', '')
                })
            # if it's a textbox, also recurse
            if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
                self.parse_obj(obj._objs, pageHeight)

            # if it's a container, recurse
            elif isinstance(obj, pdfminer.layout.LTFigure):
                print('is figure')
                self.parse_obj(obj._objs, pageHeight)

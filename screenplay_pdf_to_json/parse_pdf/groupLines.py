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

import json


class ParsePdfClass:
    def __init__(self, scriptFile):
        self.scriptFile = scriptFile

    pageWidth = 0

    newScript = {
        "pdf": []
    }

    def parsepdf(self):
        # Create a PDF parser object associated with the file object.
        parser = PDFParser(self.scriptFile)

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
        laparams = LAParams(word_margin=100, boxes_flow=1,
                            line_margin=0.3)

        # Create a PDF page aggregator object.
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)

        # Create a PDF interpreter object.
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        i = 0
        # loop over all pages in the document
        for page in PDFPage.create_pages(document):
            if i == 0:
                self.pageWidth = page.mediabox[3]

            self.newScript["pdf"].append({
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
                # text = obj.get_text()
                # if text.strip():
                #     for c in obj._objs:
                #         if isinstance(c, pdfminer.layout.LTChar):
                #             print("fontname %s" % c)

                self.newScript["pdf"][-1]["content"].append({
                    "x": round(obj.bbox[0]),
                    "y": round(pageHeight - obj.bbox[1]),
                    "text": obj.get_text().replace('\n', '').strip()
                })
            # if it's a textbox, also recurse
            if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
                self.parse_obj(obj._objs, pageHeight)

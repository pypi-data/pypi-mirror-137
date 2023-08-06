##
# File:    WatermarkUtils.py
# Author:  ep
# Date:    20-Sep-2018
# Version: 0.1
##


"""
Utility methods for combining PDF files
"""

from pdfrw import PageMerge, PdfReader, PdfWriter


class WatermarkUtils(object):
    """ Utility methods for managing watermarks
    """

    def __init__(self):
        """
        """
        pass

    def addWatermarkFile(self, fileInPath, watermarkPath, fileOutPath,
                         underneath=True):
        """Adds watermarkPath to fileInPath and output to fileOutPath

           Returns True on success.  Will raise exceptions from base on errors.

           Code based on example at
           https://github.com/pmaupin/pdfrw/blob/master/examples/watermark.py

           Same assumptions apply - pages the same size.
        """

        wmark = PageMerge().add(PdfReader(watermarkPath).pages[0])[0]
        trailer = PdfReader(fileInPath)

        for page in trailer.pages:
            PageMerge(page).add(wmark, prepend=underneath).render()

        PdfWriter(fileOutPath, trailer=trailer).write()

        return True

##
# File:    command_line.py
# Author:  ep
# Date:    20-Sep-2018
# Version: 0.1
##


import argparse
import sys

from fakepdftk.WatermarkUtils import WatermarkUtils

# Needs to support pdftk 1o08_full_validation.pdf background confidential.pdf output pdftk.pdf


def main(cmdline=None):
    if not cmdline:
        cmdline = sys.argv[1:]

    # Gross hack to ensure processing of background/output
    mangle_args = ('output', 'background')
    arguments = ['--' + arg if arg in mangle_args else arg for arg in cmdline]

    parser = argparse.ArgumentParser(description="Fake pdfTK replacement for watermarks")
    parser.add_argument("pdfin", help="PDF file to add watermark to")
    parser.add_argument("--background", required=True,
                        help="PDF file to add watermark to")
    parser.add_argument("--output", required=True,
                        help="output PDF file")

    args = parser.parse_args(arguments)

    wM = WatermarkUtils()
    status = wM.addWatermarkFile(args.pdfin, args.background,
                                 args.output)
    return status

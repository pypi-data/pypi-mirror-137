from __future__ import print_function, division, absolute_import

import os
import queue

import ddddocr
from fontTools.ttLib import TTFont
from reportlab.graphics import renderPM
from reportlab.graphics.shapes import Group, Drawing
from reportlab.graphics.shapes import Path

from ddddocr_woff.ReportLabPen import ReportLabPen


class anAlySis(object):
    def __init__(self, fontName, imagePath='images', fmt="png"):
        isExists = os.path.exists(imagePath)
        if not isExists:
            print('储存图片目录未指定并且不存在，自动创建')
            os.makedirs(imagePath)

        self.fontName = fontName
        self.imagePath = imagePath
        self.fmt = fmt
        self.font = TTFont(self.fontName)
        self.gs = self.font.getGlyphSet()

    def ttfToImage(self, transmit: queue.Queue):

        glyphNames = self.font.getGlyphOrder()

        for i in glyphNames:
            transmit.put(i)

    def text_ocr(self, transmit: queue.Queue):
        Dict = {}
        while True:
            i = transmit.get()
            if transmit.qsize() != 0:
                if i[0] == '.':  # 跳过'.notdef', '.null'
                    continue
                g = self.gs[i]
                pen = ReportLabPen(self.gs, Path())
                g.draw(pen)
                self.g = Group(pen.path)
                d = Drawing(1000, 1000)
                d.add(self.g)
                self.imageFile = self.imagePath + "/" + i + ".png"
                renderPM.drawToFile(d, self.imageFile, self.fmt)

                with open(self.imageFile, 'rb') as f:
                    png = f.read()
                ocr = ddddocr.DdddOcr()
                res = ocr.classification(png)  # png为图片路径

                Dict[i] = res
            else:
                return Dict

    def run(self):

        self.transmit = queue.Queue()
        self.ttfToImage(self.transmit)

        result = self.text_ocr(self.transmit)
        return result


if __name__ == "__main__":
    a = anAlySis(fontName="e7c2bdebed0996000411185654c80bff2288.woff").run()
    print(a)

from __future__ import print_function, division, absolute_import

import os
import queue
import threading

import ddddocr
from fontTools.ttLib import TTFont
from reportlab.graphics import renderPM
from reportlab.graphics.shapes import Group, Drawing
from reportlab.graphics.shapes import Path

from ddddocr_woff.ReportLabPen import ReportLabPen


class anAlySis(object):
    def __init__(self, fontName, imagePath='images', fmt="png", clear=False):

        if clear:
            ls = os.listdir(imagePath)
            try:
                for i in ls:
                    c_path = os.path.join(imagePath, i)
                    os.remove(c_path)
                print('缓存文件已删除')
            except:
                print('没有缓存文件')
        isExists = os.path.exists(imagePath)
        if not isExists:
            print('储存图片目录未指定并且不存在，自动创建')
            os.makedirs(imagePath)

        self.fontName = fontName
        self.imagePath = imagePath
        self.fmt = fmt
        self.font = TTFont(self.fontName)
        self.gs = self.font.getGlyphSet()
        self.transmit = queue.Queue()
        self.file = queue.Queue()
        self.Dict = {}

    def ttfToImage(self, transmit):

        glyphNames = self.font.getGlyphOrder()

        for i in glyphNames:
            transmit.put(i)

    def imges_ocr(self, transmit):

        while True:
            try:
                i = transmit.get(timeout=0.5)
                if i[0] == '.':  # 跳过'.notdef', '.null'
                    continue
                g = self.gs[i]
                pen = ReportLabPen(self.gs, Path())
                g.draw(pen)
                self.g = Group(pen.path)
                d = Drawing(2000, 2000)
                self.g.translate(200, 200)
                d.add(self.g)
                self.imageFile = self.imagePath + "/" + i + ".png"
                renderPM.drawToFile(d, self.imageFile, self.fmt)
            except:
                break

    def imges_file(self, file):

        with open(os.path.join(self.imagePath, file), 'rb') as f:
            self.text_ocr(f.read(), file)

    def text_ocr(self, png_b, file):
        ocr = ddddocr.DdddOcr()
        res = ocr.classification(png_b)
        self.Dict[file] = res

    def run(self):

        self.ttfToImage(self.transmit)

        self.imges_ocr(self.transmit)

        for file in os.listdir(self.imagePath):
            t = threading.Thread(target=self.imges_file, args=(file,))
            t.start()
            t.join()
        return self.Dict

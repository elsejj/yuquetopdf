from panflute import run_filter, Image, RawInline, Quoted, Str, LineBreak, SoftBreak
import sys
from typing import Dict,List
from hashlib import md5
from os import makedirs, path
import requests
from urllib.parse import parse_qsl
import svglib
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont



image_cahce = './cache'


def is_svg(filepath):
    exts = ["svg", "puml"]
    for ext in exts:
        if filepath.endswith(ext):
            return True
    return False



def downlaod_image(elem, doc):
    #print(elem, file=sys.stderr)
    if isinstance(elem, Image):
        img : Image = elem
        u = requests.utils.urlparse(img.url)
        attrs = dict(parse_qsl(u.fragment))
        #print(u, file=sys.stderr)
        cache_path = f'{image_cahce}{u.path}'
        if not path.exists(cache_path):
            dirs = path.split(cache_path)
            makedirs(dirs[0], exist_ok=True)
            body = requests.get(img.url, allow_redirects=True)

            with open(cache_path, 'wb') as fp:
                content = body.content
                if is_svg(cache_path):
                    content = body.content.replace(b'sans-serif', b'simhei')
                fp.write(content)
        if is_svg(cache_path):
            drawing = svg2rlg(cache_path)
            cache_path = cache_path + ".pdf"
            renderPDF.drawToFile(drawing, cache_path, canvasKwds={'initialFontName': 'simhei'})

        img.url = cache_path
        #print(attrs, file=sys.stderr)
        img.attributes['height'] = '300'
        return img
    if isinstance(elem, RawInline):
        return SoftBreak()


def main(doc=None):
    makedirs(image_cahce, exist_ok=True)
    return run_filter(downlaod_image, doc=doc)

if __name__ == "__main__":
    #svglib.DEFAULT_FONT_NAME = 'SimSun'
    #pdfmetrics.registerFont(TTFont('黑体', 'MSYHL.ttc', subfontIndex=0,asciiReadable=0))
    pdfmetrics.registerFont(TTFont('simhei', 'simhei.ttf'))
    #pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    main()
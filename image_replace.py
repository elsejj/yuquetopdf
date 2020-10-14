import sys
from os import makedirs, path
import requests
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF 
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont



image_cahce = './cache'


def is_svg(filepath):
    exts = ["svg", "puml"]
    for ext in exts:
        if filepath.endswith(ext):
            return True
    return False



def downlaod_image(imageURL):
    u = requests.utils.urlparse(imageURL)
    if u.scheme.startswith('http'):
        cache_path = f'{image_cahce}{u.path}'
    else:
        return ""
    if not path.exists(cache_path):
        dirs = path.split(cache_path)
        makedirs(dirs[0], exist_ok=True)
        body = requests.get(imageURL, allow_redirects=True)

        with open(cache_path, 'wb') as fp:
            content = body.content
            if is_svg(cache_path):
                content = body.content.replace(b'sans-serif', b'simhei')
            fp.write(content)
    if is_svg(cache_path):
        drawing = svg2rlg(cache_path)
        cache_path = cache_path + ".pdf"
        renderPDF.drawToFile(drawing, cache_path, canvasKwds={'initialFontName': 'simhei'})
    return cache_path


def main():
    if len(sys.argv) != 2:
        print("a url is required", sys.argv,  file=sys.stderr)
        return
    makedirs(image_cahce, exist_ok=True)
    local_path = downlaod_image(sys.argv[1])
    print(local_path,end="")

if __name__ == "__main__":
    pdfmetrics.registerFont(TTFont('simhei', 'simhei.ttf'))
    main()
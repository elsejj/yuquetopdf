import sys
import subprocess 
import os.path
import re
import shutil
import datetime
import os


FONT_NAME = '思源黑体'
AUTHOR_NAME = '钒钛智能'
PANDOC = os.getenv("PANDOC_EXE") or "pandoc"


mdtitle = """
---
title: '{0}'
author: {1}
date: {2}
---

"""

def docDate():
    now = datetime.datetime.now()
    return now.strftime("%Y.%m")
    
    

def format_md(iname, oname):
    fin = open(iname)
    fout = open(oname, "w")

    href = re.compile(r'<a.*?>.*?</a>')
    br = re.compile(r'<br\s*/>')
    tag = re.compile(r'{.*}')

    firstTitle = False # use first title as document title

    for l in fin:

        if not firstTitle and l.startswith("# ") :
            firstTitle = True
            title = l[2:].strip()
            print(mdtitle.format(title, AUTHOR_NAME, docDate()), file=fout)
            continue

        #text = '\n\n'.join(br.split(l))
        text = l
        if href.match(text) == None:
            print(text, file=fout, end='')
        else:
            print("\n\n", file=fout, end='')
    
    fin.close()
    fout.close()


def main():

    if len(sys.argv) < 2:
        print("a input file is required")
        return

    outfmt = '.pdf'

    if len(sys.argv) > 2:
        outfmt = "." + sys.argv[2]

    ifname = sys.argv[1]
    pos = ifname.rindex('.')
    ofname = ifname[0:pos] + outfmt
    ffname = ifname[0:pos] + ".fmt." + ifname[pos+1:]

    if ifname.endswith(".md", ):
        format_md(ifname, ffname)
    else:
        shutil.copy(ifname, ffname)

        
    cmd = [
        PANDOC,
        ffname,
        "-o",
        ofname,
        "--lua-filter",  "yuque.lua",
        "--template", "./fantai.tex",
        "--pdf-engine=xelatex",
        "--toc", "-N",
        '-V geometry:"top=2cm, bottom=1.5cm, left=2cm, right=2cm"',
        "-V", f"CJKmainfont={FONT_NAME}",
        "-V", f"mainfont={FONT_NAME}",
        "-V", f"fontsize=14pt",
        "-V", f"logo=./logo.png",
        "-V", "colorlinks"
    ]
    print(' '.join(cmd))
    #print(cmd)
    subprocess.run(cmd)
    #os.remove(ffname)

    

if __name__ == "__main__":
    main()
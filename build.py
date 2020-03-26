import sys
import subprocess 
import os.path
import re
import shutil
import datetime


FONT_NAME = '思源黑体'
#FONT_NAME = '仿宋'


mdtitle = """
---
title: '{0}'
author: 钒钛智能
date: {1}
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

    firstTitle1 = False

    for l in fin:

        if not firstTitle1 and l.startswith("# ") :
            firstTitle1 = True
            title = l[2:].strip()
            print(mdtitle.format(title, docDate()), file=fout)
            continue

        text = '\n\n'.join(br.split(l))
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

    if ifname.endswith(".md"):
        format_md(ifname, ffname)
    else:
        shutil.copy(ifname, ffname)

        
    cmd = [
        'pandoc',
        ffname,
        "-o",
        ofname,
        "--filter",  "./yuque.py",
        "--template", "./fantai.tex",
        "--pdf-engine=xelatex",
        "--toc",
        "-V", f"CJKmainfont={FONT_NAME}",
        "-V", f"mainfont={FONT_NAME}",
        "-V", f"fontsize=14pt",
        "-V", f"logo=./logo.png",
    ]
    print(' '.join(cmd))
    #print(cmd)
    subprocess.run(cmd)
    #os.remove(ffname)

    

if __name__ == "__main__":
    main()
import shutil
from functions import generate_page
from functions import generate_pages_recursive
import sys
import os

def main():

    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    if os.path.exists("docs"):
        shutil.rmtree("docs")
    shutil.copytree("static", "docs")

    generate_pages_recursive("content", "template.html", "docs", basepath)

    

if __name__ == "__main__":
    main()
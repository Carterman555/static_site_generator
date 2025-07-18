import shutil
from functions import generate_page
from functions import generate_pages_recursive

def main():
    shutil.rmtree("public")
    shutil.copytree("static", "public")

    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()